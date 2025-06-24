import pytest
from pydantic import ValidationError
from src.domain.value_objects.task_status import TaskStatus, TaskStatusEnum


class TestTaskStatus:
    """Test cases for TaskStatus value object."""

    def test_valid_task_status_creation_from_enum(self):
        """Test creating TaskStatus from enum."""
        status = TaskStatus(value=TaskStatusEnum.PENDING)
        assert status.value == TaskStatusEnum.PENDING

    def test_valid_task_status_creation_from_string(self):
        """Test creating TaskStatus from string."""
        status = TaskStatus(value="pending")
        assert status.value == TaskStatusEnum.PENDING

    def test_task_status_string_representation(self):
        """Test TaskStatus string representation."""
        status = TaskStatus(value=TaskStatusEnum.COMPLETED)
        assert str(status) == "completed"

    def test_task_status_equality(self):
        """Test TaskStatus equality comparison."""
        status1 = TaskStatus(value=TaskStatusEnum.PENDING)
        status2 = TaskStatus(value="pending")
        status3 = TaskStatus(value=TaskStatusEnum.COMPLETED)

        assert status1 == status2
        assert status1 != status3
        assert status1 != "not_a_status"

    def test_task_status_hash(self):
        """Test TaskStatus can be used as dictionary key."""
        status1 = TaskStatus(value=TaskStatusEnum.PENDING)
        status2 = TaskStatus(value="pending")
        status3 = TaskStatus(value=TaskStatusEnum.COMPLETED)

        status_dict = {status1: "pending_tasks"}
        assert status_dict[status2] == "pending_tasks"  # Same hash

        assert hash(status1) == hash(status2)
        assert hash(status1) != hash(status3)

    def test_invalid_task_status_raises_validation_error(self):
        """Test that invalid task status raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TaskStatus(value="invalid_status")

        assert (
            "Input should be 'pending', 'in_progress', 'completed' or 'cancelled'"
            in str(exc_info.value)
        )

    def test_numeric_task_status_raises_validation_error(self):
        """Test that numeric task status raises ValidationError."""
        with pytest.raises(ValidationError):
            TaskStatus(value=123)

    def test_is_completed_method(self):
        """Test is_completed method."""
        completed_status = TaskStatus(value=TaskStatusEnum.COMPLETED)
        pending_status = TaskStatus(value=TaskStatusEnum.PENDING)

        assert completed_status.is_completed() is True
        assert pending_status.is_completed() is False

    def test_is_pending_method(self):
        """Test is_pending method."""
        pending_status = TaskStatus(value=TaskStatusEnum.PENDING)
        completed_status = TaskStatus(value=TaskStatusEnum.COMPLETED)

        assert pending_status.is_pending() is True
        assert completed_status.is_pending() is False

    def test_can_transition_to_valid_transitions(self):
        """Test valid status transitions."""
        pending = TaskStatus(value=TaskStatusEnum.PENDING)
        in_progress = TaskStatus(value=TaskStatusEnum.IN_PROGRESS)
        completed = TaskStatus(value=TaskStatusEnum.COMPLETED)
        cancelled = TaskStatus(value=TaskStatusEnum.CANCELLED)

        # From PENDING
        assert pending.can_transition_to(in_progress) is True
        assert pending.can_transition_to(cancelled) is True
        assert pending.can_transition_to(completed) is False

        # From IN_PROGRESS
        assert in_progress.can_transition_to(completed) is True
        assert in_progress.can_transition_to(cancelled) is True
        assert in_progress.can_transition_to(pending) is True

        # From COMPLETED (no transitions allowed)
        assert completed.can_transition_to(pending) is False
        assert completed.can_transition_to(in_progress) is False
        assert completed.can_transition_to(cancelled) is False

        # From CANCELLED
        assert cancelled.can_transition_to(pending) is True
        assert cancelled.can_transition_to(in_progress) is False
        assert cancelled.can_transition_to(completed) is False

    @pytest.mark.parametrize(
        "status_value,expected_enum",
        [
            ("pending", TaskStatusEnum.PENDING),
            ("in_progress", TaskStatusEnum.IN_PROGRESS),
            ("completed", TaskStatusEnum.COMPLETED),
            ("cancelled", TaskStatusEnum.CANCELLED),
        ],
    )
    def test_various_valid_status_strings(self, status_value, expected_enum):
        """Test various valid status string values."""
        status = TaskStatus(value=status_value)
        assert status.value == expected_enum

    @pytest.mark.parametrize(
        "invalid_status",
        [
            "invalid",
            "",
            "PENDING",  # Case sensitive
            "done",
            "started",
        ],
    )
    def test_various_invalid_status_strings(self, invalid_status):
        """Test various invalid status string values."""
        with pytest.raises(ValidationError):
            TaskStatus(value=invalid_status)
