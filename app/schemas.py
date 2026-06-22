from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, EmailStr

class PROGRESS(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"


class PRIORITY(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Tasks(BaseModel):
    title: str
    description: str | None = None

    priority:  PRIORITY = PRIORITY.MEDIUM
    progress: PROGRESS = PROGRESS.PENDING

    due_date: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None
class TaskCreate(Tasks):
    pass


class Task(Tasks):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)



class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")


class User(UserBase):
    id: int
    is_active: bool
    tasks: list[Task] = []

    model_config = ConfigDict(from_attributes=True)
