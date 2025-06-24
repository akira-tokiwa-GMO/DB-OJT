import pytest
from datetime import datetime
from pydantic import ValidationError
from src.domain.entities.user import User
from src.domain.value_objects.email import Email


class TestUser:
    """Test cases for User entity."""

    def test_user_creation_with_minimal_data(self):
        """Test creating a user with minimal required data."""
        email = Email(value="test@example.com")
        user = User(name="Test User", email=email)

        assert user.name == "Test User"
        assert user.email == email
        assert user.is_active is True
        assert user.id is None
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_user_creation_with_full_data(self):
        """Test creating a user with all data."""
        email = Email(value="test@example.com")
        user = User(id=1, name="Full User", email=email, is_active=False)

        assert user.id == 1
        assert user.name == "Full User"
        assert user.email == email
        assert user.is_active is False

    def test_empty_name_raises_validation_error(self):
        """Test that empty name raises ValidationError."""
        email = Email(value="test@example.com")

        with pytest.raises(ValidationError) as exc_info:
            User(name="", email=email)

        assert "String should have at least 1 character" in str(exc_info.value)

    def test_whitespace_name_raises_validation_error(self):
        """Test that whitespace-only name raises ValidationError."""
        email = Email(value="test@example.com")

        with pytest.raises(ValidationError) as exc_info:
            User(name="   ", email=email)

        assert "Name cannot be empty" in str(exc_info.value)

    def test_name_trimming(self):
        """Test that name is properly trimmed."""
        email = Email(value="test@example.com")
        user = User(name="  Test User  ", email=email)

        assert user.name == "Test User"

    def test_update_name(self):
        """Test updating user name."""
        email = Email(value="test@example.com")
        user = User(name="Original Name", email=email)

        original_updated_at = user.updated_at
        user.update_name("New Name")

        assert user.name == "New Name"
        assert user.updated_at > original_updated_at

    def test_update_name_empty_raises_error(self):
        """Test updating user name with empty string raises error."""
        email = Email(value="test@example.com")
        user = User(name="Original Name", email=email)

        with pytest.raises(ValueError) as exc_info:
            user.update_name("")

        assert "Name cannot be empty" in str(exc_info.value)

    def test_update_name_whitespace_raises_error(self):
        """Test updating user name with whitespace raises error."""
        email = Email(value="test@example.com")
        user = User(name="Original Name", email=email)

        with pytest.raises(ValueError) as exc_info:
            user.update_name("   ")

        assert "Name cannot be empty" in str(exc_info.value)

    def test_update_name_trimming(self):
        """Test updating user name with trimming."""
        email = Email(value="test@example.com")
        user = User(name="Original Name", email=email)

        user.update_name("  New Name  ")
        assert user.name == "New Name"

    def test_deactivate_user(self):
        """Test deactivating user account."""
        email = Email(value="test@example.com")
        user = User(name="Test User", email=email)

        assert user.is_active is True

        original_updated_at = user.updated_at
        user.deactivate()

        assert user.is_active is False
        assert user.updated_at > original_updated_at

    def test_activate_user(self):
        """Test activating user account."""
        email = Email(value="test@example.com")
        user = User(name="Test User", email=email, is_active=False)

        assert user.is_active is False

        original_updated_at = user.updated_at
        user.activate()

        assert user.is_active is True
        assert user.updated_at > original_updated_at

    def test_user_equality_with_same_id(self):
        """Test user equality with same ID."""
        email1 = Email(value="test1@example.com")
        email2 = Email(value="test2@example.com")

        user1 = User(id=1, name="User 1", email=email1)
        user2 = User(id=1, name="User 2", email=email2)

        assert user1 == user2

    def test_user_equality_with_different_id(self):
        """Test user equality with different ID."""
        email1 = Email(value="test1@example.com")
        email2 = Email(value="test2@example.com")

        user1 = User(id=1, name="User 1", email=email1)
        user2 = User(id=2, name="User 2", email=email2)

        assert user1 != user2

    def test_user_equality_with_no_id_same_email(self):
        """Test user equality when no ID is set but same email."""
        email = Email(value="test@example.com")

        user1 = User(name="User 1", email=email)
        user2 = User(name="User 2", email=email)

        assert user1 == user2

    def test_user_equality_with_no_id_different_email(self):
        """Test user equality when no ID is set and different email."""
        email1 = Email(value="test1@example.com")
        email2 = Email(value="test2@example.com")

        user1 = User(name="User 1", email=email1)
        user2 = User(name="User 2", email=email2)

        assert user1 != user2

    def test_user_equality_with_non_user_object(self):
        """Test user equality with non-User object."""
        email = Email(value="test@example.com")
        user = User(name="Test User", email=email)

        assert user != "not_a_user"
        assert user != 123
        assert user is not None

    def test_user_hash_with_id(self):
        """Test user hash with ID."""
        email1 = Email(value="test1@example.com")
        email2 = Email(value="test2@example.com")

        user1 = User(id=1, name="User 1", email=email1)
        user2 = User(id=1, name="User 2", email=email2)

        assert hash(user1) == hash(user2)

    def test_user_hash_without_id(self):
        """Test user hash without ID."""
        email = Email(value="test@example.com")

        user1 = User(name="User 1", email=email)
        user2 = User(name="User 2", email=email)

        assert hash(user1) == hash(user2)

    def test_user_hash_different_emails(self):
        """Test user hash with different emails."""
        email1 = Email(value="test1@example.com")
        email2 = Email(value="test2@example.com")

        user1 = User(name="User 1", email=email1)
        user2 = User(name="User 2", email=email2)

        assert hash(user1) != hash(user2)

    @pytest.mark.parametrize(
        "name,expected",
        [
            ("John Doe", "John Doe"),
            ("  Alice  ", "Alice"),
            ("Bob Smith Jr.", "Bob Smith Jr."),
        ],
    )
    def test_various_valid_names(self, name, expected):
        """Test various valid name formats."""
        email = Email(value="test@example.com")
        user = User(name=name, email=email)

        assert user.name == expected
