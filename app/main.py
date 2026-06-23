from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import auth
from app import crud
from app import models
from app import schemas
from app.database import engine, get_db
from app.logging_config import get_logger

logger = get_logger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_access_token(token)
    if not payload or "sub" not in payload:
        logger.warning("Invalid token received")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email = payload.get("sub")
    user = crud.get_user_by_email(db, email=email)
    if not user:
        logger.warning(f"User not found for email: {email}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



# AUTH & USER ROUTES
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    logger.info(f"User logged in: {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        logger.warning(f"Registration failed, email already registered: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(db=db, user=user)
    logger.info(f"User registered: {new_user.email}")
    return new_user


@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user



# TASK ROUTES
@app.post("/tasks/", response_model=schemas.Task)
def create_task(
        item: schemas.TaskCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user)  # Secured!
):
    """Create a task for the currently authenticated user."""
    return crud.create_user_task(db=db, item=item, user_id=current_user.id)


@app.get("/tasks/", response_model=list[schemas.Task])
def read_my_tasks(
        skip: int = 0,
        limit: int = 50,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user)  # Secured
):
    """Fetch only the logged-in user's tasks."""
    return crud.get_user_tasks(db, user_id=current_user.id, skip=skip, limit=limit)


@app.get("/tasks/status/{progress_status}", response_model=list[schemas.Task])
def read_tasks_by_status(
        progress_status: schemas.PROGRESS,
        skip: int = 0,
        limit: int = 50,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user)
):
    """Filter the logged-in user's tasks by progress (pending, active, completed)."""
    return crud.get_user_tasks_by_progress(
        db, user_id=current_user.id, progress=progress_status, skip=skip, limit=limit
    )


@app.patch("/tasks/{task_id}/progress", response_model=schemas.Task)
def update_task_status(
        task_id: int,
        new_status: schemas.PROGRESS,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user)
):
    """Update a task's status if it belongs to the current user."""
    db_task = crud.get_task_by_id(db, task_id=task_id)
    if not db_task or db_task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")

    return crud.update_task_progress(db, task_id=task_id, new_progress=new_status)


@app.delete("/tasks/{task_id}")
def delete_user_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user)
):
    """Delete a task if it belongs to the current user."""
    db_task = crud.get_task_by_id(db, task_id=task_id)
    if not db_task or db_task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")

    crud.delete_task(db, task_id=task_id)
    return {"detail": "Task deleted successfully"}

@app.post("/tasks/{task_id}/restore", response_model=schemas.Task)
def restore_user_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Restore soft-deleted task."""
    restored_task = crud.restore_task(db, task_id=task_id)
    if not restored_task or restored_task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    return restored_task