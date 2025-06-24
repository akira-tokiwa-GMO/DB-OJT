from enum import Enum
from pydantic import BaseModel, field_validator
from typing import Any


class TaskStatusEnum(str, Enum):
    """Task status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskStatus(BaseModel):
    """Task status value object."""

    value: TaskStatusEnum

    @field_validator("value")
    @classmethod
    def validate_status(cls, v: Any) -> TaskStatusEnum:
        if isinstance(v, str):
            try:
                return TaskStatusEnum(v)
            except ValueError:
                raise ValueError(f"Invalid task status: {v}")
        elif isinstance(v, TaskStatusEnum):
            return v
        else:
            raise ValueError("Task status must be a string or TaskStatusEnum")

    def __str__(self) -> str:
        return self.value.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TaskStatus):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def is_completed(self) -> bool:
        return self.value == TaskStatusEnum.COMPLETED

    def is_pending(self) -> bool:
        return self.value == TaskStatusEnum.PENDING

    def can_transition_to(self, new_status: "TaskStatus") -> bool:
        """Check if transition to new status is valid."""
        transitions = {
            TaskStatusEnum.PENDING: [
                TaskStatusEnum.IN_PROGRESS,
                TaskStatusEnum.CANCELLED,
            ],
            TaskStatusEnum.IN_PROGRESS: [
                TaskStatusEnum.COMPLETED,
                TaskStatusEnum.CANCELLED,
                TaskStatusEnum.PENDING,
            ],
            TaskStatusEnum.COMPLETED: [],  # No transitions from completed
            TaskStatusEnum.CANCELLED: [
                TaskStatusEnum.PENDING
            ],  # Can reopen cancelled tasks
        }
        return new_status.value in transitions.get(self.value, [])
