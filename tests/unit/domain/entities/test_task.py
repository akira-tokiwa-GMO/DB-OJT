import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError
from src.domain.entities.task import Task
from src.domain.value_objects.task_id import TaskId
from src.domain.value_objects.task_status import TaskStatus, TaskStatusEnum
from src.domain.value_objects.email import Email


class TestTask:
    """Test cases for Task entity."""

    def test_task_creation_with_minimal_data(self):
        """Test creating a task with minimal required data."""
        task = Task(title="Test Task")

        assert task.title == "Test Task"
        assert task.description is None
        assert task.status.value == TaskStatusEnum.PENDING
        assert task.assignee_email is None
        assert task.id is None
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)
        assert task.due_date is None

    def test_task_creation_with_full_data(self):
        """Test creating a task with all data."""
        task_id = TaskId(value=1)
        email = Email(value="test@example.com")
        status = TaskStatus(value=TaskStatusEnum.IN_PROGRESS)
        due_date = datetime.utcnow() + timedelta(days=1)

        task = Task(
            id=task_id,
            title="Full Task",
            description="A complete task",
            status=status,
            assignee_email=email,
            due_date=due_date,
        )

        assert task.id == task_id
        assert task.title == "Full Task"
        assert task.description == "A complete task"
        assert task.status == status
        assert task.assignee_email == email
        assert task.due_date == due_date

    def test_empty_title_raises_validation_error(self):
        """Test that empty title raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Task(title="")

        assert "String should have at least 1 character" in str(exc_info.value)

    def test_whitespace_title_raises_validation_error(self):
        """Test that whitespace-only title raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Task(title="   ")

        assert "Title cannot be empty" in str(exc_info.value)

    def test_title_trimming(self):
        """Test that title is properly trimmed."""
        task = Task(title="  Test Task  ")
        assert task.title == "Test Task"

    def test_description_trimming(self):
        """Test that description is properly trimmed."""
        task = Task(title="Test", description="  Test Description  ")
        assert task.description == "Test Description"

    def test_empty_description_becomes_none(self):
        """Test that empty description becomes None."""
        task = Task(title="Test", description="   ")
        assert task.description is None

    def test_due_date_in_past_raises_validation_error(self):
        """Test that due date in the past raises ValidationError."""
        past_date = datetime.utcnow() - timedelta(days=1)

        with pytest.raises(ValidationError) as exc_info:
            Task(title="Test", due_date=past_date)

        assert "Due date cannot be in the past" in str(exc_info.value)

    def test_update_status_valid_transition(self):
        """Test updating task status with valid transition."""
        task = Task(title="Test Task")
        new_status = TaskStatus(value=TaskStatusEnum.IN_PROGRESS)

        original_updated_at = task.updated_at
        task.update_status(new_status)

        assert task.status == new_status
        assert task.updated_at > original_updated_at

    def test_update_status_invalid_transition_raises_error(self):
        """Test updating task status with invalid transition."""
        task = Task(
            title="Test Task", status=TaskStatus(value=TaskStatusEnum.COMPLETED)
        )
        new_status = TaskStatus(value=TaskStatusEnum.IN_PROGRESS)

        with pytest.raises(ValueError) as exc_info:
            task.update_status(new_status)

        assert "Cannot transition from" in str(exc_info.value)

    def test_assign_to_user(self):
        """Test assigning task to a user."""
        task = Task(title="Test Task")
        email = Email(value="user@example.com")

        original_updated_at = task.updated_at
        task.assign_to(email)

        assert task.assignee_email == email
        assert task.updated_at > original_updated_at

    def test_update_title(self):
        """Test updating task title."""
        task = Task(title="Original Title")

        original_updated_at = task.updated_at
        task.update_title("New Title")

        assert task.title == "New Title"
        assert task.updated_at > original_updated_at

    def test_update_title_empty_raises_error(self):
        """Test updating task title with empty string raises error."""
        task = Task(title="Original Title")

        with pytest.raises(ValueError) as exc_info:
            task.update_title("")

        assert "Title cannot be empty" in str(exc_info.value)

    def test_update_description(self):
        """Test updating task description."""
        task = Task(title="Test Task")

        original_updated_at = task.updated_at
        task.update_description("New description")

        assert task.description == "New description"
        assert task.updated_at > original_updated_at

    def test_update_description_empty_becomes_none(self):
        """Test updating description with empty string becomes None."""
        task = Task(title="Test Task", description="Original")

        task.update_description("   ")
        assert task.description is None

    def test_set_due_date(self):
        """Test setting task due date."""
        task = Task(title="Test Task")
        future_date = datetime.utcnow() + timedelta(days=1)

        original_updated_at = task.updated_at
        task.set_due_date(future_date)

        assert task.due_date == future_date
        assert task.updated_at > original_updated_at

    def test_set_due_date_past_raises_error(self):
        """Test setting due date in past raises error."""
        task = Task(title="Test Task")
        past_date = datetime.utcnow() - timedelta(days=1)

        with pytest.raises(ValueError) as exc_info:
            task.set_due_date(past_date)

        assert "Due date cannot be in the past" in str(exc_info.value)

    def test_is_overdue_with_past_due_date(self):
        """Test is_overdue returns True for past due date."""
        past_date = datetime.utcnow() - timedelta(hours=1)
        task = Task(title="Test Task")
        task.due_date = past_date  # Set directly to bypass validation

        assert task.is_overdue() is True

    def test_is_overdue_with_future_due_date(self):
        """Test is_overdue returns False for future due date."""
        future_date = datetime.utcnow() + timedelta(days=1)
        task = Task(title="Test Task", due_date=future_date)

        assert task.is_overdue() is False

    def test_is_overdue_with_no_due_date(self):
        """Test is_overdue returns False when no due date set."""
        task = Task(title="Test Task")

        assert task.is_overdue() is False

    def test_is_overdue_completed_task_not_overdue(self):
        """Test completed task is not overdue even with past due date."""
        past_date = datetime.utcnow() - timedelta(hours=1)
        task = Task(
            title="Test Task", status=TaskStatus(value=TaskStatusEnum.COMPLETED)
        )
        task.due_date = past_date  # Set directly to bypass validation

        assert task.is_overdue() is False

    def test_task_equality_with_same_id(self):
        """Test task equality with same ID."""
        task_id = TaskId(value=1)
        task1 = Task(id=task_id, title="Task 1")
        task2 = Task(id=task_id, title="Task 2")

        assert task1 == task2

    def test_task_equality_with_different_id(self):
        """Test task equality with different ID."""
        task1 = Task(id=TaskId(value=1), title="Task 1")
        task2 = Task(id=TaskId(value=2), title="Task 2")

        assert task1 != task2

    def test_task_equality_with_no_id(self):
        """Test task equality when no ID is set."""
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")

        assert task1 != task2

    def test_task_hash_with_id(self):
        """Test task hash with ID."""
        task_id = TaskId(value=1)
        task1 = Task(id=task_id, title="Task 1")
        task2 = Task(id=task_id, title="Task 2")

        assert hash(task1) == hash(task2)

    def test_task_hash_without_id(self):
        """Test task hash without ID."""
        task = Task(title="Test Task")

        # Should not raise exception
        hash_value = hash(task)
        assert isinstance(hash_value, int)
