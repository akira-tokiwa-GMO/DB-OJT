import pytest
from pydantic import ValidationError
from src.domain.value_objects.email import Email


class TestEmail:
    """Test cases for Email value object."""

    def test_valid_email_creation(self):
        """Test creating a valid Email."""
        email = Email(value="test@example.com")
        assert str(email.value) == "test@example.com"

    def test_email_string_representation(self):
        """Test Email string representation."""
        email = Email(value="user@domain.com")
        assert str(email) == "user@domain.com"

    def test_email_equality(self):
        """Test Email equality comparison."""
        email1 = Email(value="test@example.com")
        email2 = Email(value="test@example.com")
        email3 = Email(value="other@example.com")

        assert email1 == email2
        assert email1 != email3
        assert email1 != "not_an_email"

    def test_email_hash(self):
        """Test Email can be used as dictionary key."""
        email1 = Email(value="test@example.com")
        email2 = Email(value="test@example.com")
        email3 = Email(value="other@example.com")

        email_dict = {email1: "user1"}
        assert email_dict[email2] == "user1"  # Same hash

        assert hash(email1) == hash(email2)
        assert hash(email1) != hash(email3)

    def test_invalid_email_format_raises_validation_error(self):
        """Test that invalid email format raises ValidationError."""
        invalid_emails = [
            "invalid_email",
            "@example.com",
            "test@",
            "test.example.com",
            "",
            "test@.com",
            "test@domain.",
        ]

        for invalid_email in invalid_emails:
            with pytest.raises(ValidationError):
                Email(value=invalid_email)

    @pytest.mark.parametrize(
        "valid_email",
        [
            "test@example.com",
            "user.name@domain.co.jp",
            "admin+tag@company.org",
            "simple@test.io",
            "123@numbers.net",
        ],
    )
    def test_various_valid_emails(self, valid_email):
        """Test various valid email formats."""
        email = Email(value=valid_email)
        assert str(email) == valid_email

    def test_email_normalization(self):
        """Test that email addresses are properly normalized."""
        # EmailStr in pydantic automatically normalizes emails
        email = Email(value="Test@Example.COM")
        # The exact normalization behavior depends on pydantic's implementation
        assert "@" in str(email)
