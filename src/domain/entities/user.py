from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from ..value_objects.email import Email


class User(BaseModel):
    """User entity representing a user in the system."""

    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    email: Email
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    def update_name(self, new_name: str) -> None:
        """Update user name."""
        if not new_name or not new_name.strip():
            raise ValueError("Name cannot be empty")
        self.name = new_name.strip()
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        """Deactivate user account."""
        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self) -> None:
        """Activate user account."""
        self.is_active = True
        self.updated_at = datetime.now()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        if self.id is None or other.id is None:
            return self.email == other.email
        return self.id == other.id

    def __hash__(self) -> int:
        if self.id is None:
            return hash(self.email)
        return hash(self.id)
