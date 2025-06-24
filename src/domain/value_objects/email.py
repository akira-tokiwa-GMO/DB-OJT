from pydantic import BaseModel, EmailStr


class Email(BaseModel):
    """Email value object with validation."""

    value: EmailStr

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Email):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
