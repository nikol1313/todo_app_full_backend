#1. imports
from sqlalchemy import ForeignKey, String, DateTime, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.schemas import PROGRESS, PRIORITY
from datetime import datetime


#2. creating tables
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)

    tasks: Mapped[list["Tasks"]] = relationship(back_populates="owner")
    notes: Mapped[list["Notes"]] = relationship(back_populates="owner")


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)

    priority: Mapped[PRIORITY] = mapped_column(Enum(PRIORITY), default=PRIORITY.MEDIUM)
    progress: Mapped[PROGRESS] = mapped_column(Enum(PROGRESS), default=PROGRESS.PENDING)

    due_date: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)

    description: Mapped[str | None] = mapped_column(String, index=True, default=None)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="tasks")

class Notes(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, default=None)
    content: Mapped[str] = mapped_column(String, default=None)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="notes")





