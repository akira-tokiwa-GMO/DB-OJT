from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from ..value_objects.task_id import TaskId
from ..value_objects.task_status import TaskStatus, TaskStatusEnum
from ..value_objects.email import Email


class Task(BaseModel):
    """Task entity representing a task in the task management system."""

    id: Optional[TaskId] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = Field(
        default_factory=lambda: TaskStatus(value=TaskStatusEnum.PENDING)
    )
    assignee_email: Optional[Email] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    due_date: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return v.strip() if v.strip() else None
        return v

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None and v < datetime.now():
            raise ValueError("Due date cannot be in the past")
        return v

    def update_status(self, new_status: TaskStatus) -> None:
        """Update task status with validation."""
        if not self.status.can_transition_to(new_status):
            raise ValueError(f"Cannot transition from {self.status} to {new_status}")
        self.status = new_status
        self.updated_at = datetime.now()

    def assign_to(self, email: Email) -> None:
        """Assign task to a user."""
        self.assignee_email = email
        self.updated_at = datetime.now()

    def update_title(self, new_title: str) -> None:
        """Update task title."""
        if not new_title or not new_title.strip():
            raise ValueError("Title cannot be empty")
        self.title = new_title.strip()
        self.updated_at = datetime.now()

    def update_description(self, new_description: Optional[str]) -> None:
        """Update task description."""
        self.description = (
            new_description.strip()
            if new_description and new_description.strip()
            else None
        )
        self.updated_at = datetime.now()

    def set_due_date(self, due_date: Optional[datetime]) -> None:
        """Set task due date."""
        if due_date is not None and due_date < datetime.now():
            raise ValueError("Due date cannot be in the past")
        self.due_date = due_date
        self.updated_at = datetime.now()

    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.due_date is None:
            return False
        return datetime.now() > self.due_date and not self.status.is_completed()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return False
        if self.id is None or other.id is None:
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        if self.id is None:
            return hash((self.title, self.created_at))
        return hash(self.id)
