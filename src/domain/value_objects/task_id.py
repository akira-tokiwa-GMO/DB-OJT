from typing import Any
from pydantic import BaseModel, field_validator


class TaskId(BaseModel):
    """Task ID value object."""

    value: int

    @field_validator("value")
    @classmethod
    def validate_positive(cls, v: Any) -> int:
        if not isinstance(v, int):
            raise ValueError("Task ID must be an integer")
        if v <= 0:
            raise ValueError("Task ID must be positive")
        return v

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TaskId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
