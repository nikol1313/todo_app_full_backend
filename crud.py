from sqlalchemy.orm import Session
from auth import get_password_hash
import models
import schemas


from sqlalchemy.orm import Session
from auth import get_password_hash
import models
import schemas
from logging_config import get_logger

logger = get_logger(__name__)

# USER CRUD
def get_user(db: Session, user_id: int):
    """get user by its id"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        logger.info(f"User not found: {user_id}")
    return user


def get_user_by_email(db: Session, email: str):
    """get user by its email"""
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        logger.info(f"User lookup failed for email: {email}")
    return user


def get_users(db: Session, skip: int = 0, limit: int = 50):
    """fetch all users"""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """create user"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created in DB: {db_user.email}")
    return db_user



# TASK CRUD
def get_task_by_id(db: Session, task_id: int):
    """fetch task by id"""
    return db.query(models.Tasks).filter(models.Tasks.id == task_id).first()


def get_user_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 50):
    """fetch task by user id"""
    return db.query(models.Tasks).filter(models.Tasks.owner_id == user_id).offset(skip).limit(limit).all()


def create_user_task(db: Session, item: schemas.TaskCreate, user_id: int):
    """create task for user"""
    db_item = models.Tasks(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_task_progress(db: Session, task_id: int, new_progress: schemas.PROGRESS):
    """update task's status"""
    db_task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    if db_task:
        db_task.progress = new_progress
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    """delete task by id"""
    db_task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False

def get_user_tasks_by_progress(db: Session, user_id: int, progress: schemas.PROGRESS, skip: int = 0, limit: int = 50):
    """Fetch user's tasks that match a specific status"""
    return db.query(models.Tasks).filter(
        models.Tasks.owner_id == user_id,
        models.Tasks.progress == progress
    ).offset(skip).limit(limit).all()