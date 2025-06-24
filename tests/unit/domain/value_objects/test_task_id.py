import pytest
from pydantic import ValidationError
from src.domain.value_objects.task_id import TaskId


class TestTaskId:
    """Test cases for TaskId value object."""

    def test_valid_task_id_creation(self):
        """Test creating a valid TaskId."""
        task_id = TaskId(value=1)
        assert task_id.value == 1

    def test_task_id_string_representation(self):
        """Test TaskId string representation."""
        task_id = TaskId(value=42)
        assert str(task_id) == "42"

    def test_task_id_equality(self):
        """Test TaskId equality comparison."""
        task_id1 = TaskId(value=1)
        task_id2 = TaskId(value=1)
        task_id3 = TaskId(value=2)

        assert task_id1 == task_id2
        assert task_id1 != task_id3
        assert task_id1 != "not_a_task_id"

    def test_task_id_hash(self):
        """Test TaskId can be used as dictionary key."""
        task_id1 = TaskId(value=1)
        task_id2 = TaskId(value=1)
        task_id3 = TaskId(value=2)

        task_dict = {task_id1: "task1"}
        assert task_dict[task_id2] == "task1"  # Same hash

        assert hash(task_id1) == hash(task_id2)
        assert hash(task_id1) != hash(task_id3)

    def test_zero_task_id_raises_validation_error(self):
        """Test that zero TaskId raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TaskId(value=0)

        assert "Task ID must be positive" in str(exc_info.value)

    def test_negative_task_id_raises_validation_error(self):
        """Test that negative TaskId raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TaskId(value=-1)

        assert "Task ID must be positive" in str(exc_info.value)

    def test_non_integer_task_id_raises_validation_error(self):
        """Test that non-integer TaskId raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TaskId(value="not_an_integer")

        assert "Input should be a valid integer" in str(exc_info.value)

    def test_float_task_id_raises_validation_error(self):
        """Test that float TaskId raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TaskId(value=1.5)

        assert "Input should be a valid integer" in str(exc_info.value)

    @pytest.mark.parametrize("valid_id", [1, 2, 100, 999999])
    def test_various_valid_task_ids(self, valid_id):
        """Test various valid TaskId values."""
        task_id = TaskId(value=valid_id)
        assert task_id.value == valid_id

    @pytest.mark.parametrize("invalid_id", [0, -1, -100])
    def test_various_invalid_task_ids(self, invalid_id):
        """Test various invalid TaskId values."""
        with pytest.raises(ValidationError):
            TaskId(value=invalid_id)
