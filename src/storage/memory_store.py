"""In-memory task storage for the broker.

This module stores task records in Python data structures while the broker
is running. It is simple and fast, but data is lost when the process exits.
"""

from collections import deque

from src.models.task import (
    TaskCompleteRequest,
    TaskCreateRequest,
    TaskFailRequest,
    TaskRecord,
    TaskStatus,
)


class MemoryTaskStore:
    """In-memory storage backend for task records.

    This store keeps all tasks in a dictionary and tracks pending task IDs in a
    queue so workers can claim tasks in FIFO order.
    """

    def __init__(self) -> None:
        """Initialize empty task storage."""
        self.tasks: dict[str, TaskRecord] = {}
        self.pending_queue: deque[str] = deque()
    
    def create_task(self, request: TaskCreateRequest) -> TaskRecord:
        """Create and store a new pending task.
        
        Args:
            request: Client request containing the task name and arguments.
        
        Returns:
            The created task record.
        """
        task = TaskRecord(
            name=request.name,
            args=request.args,
        )

        self.tasks[task.id] = task
        self.pending_queue.append(task.id)

        return task
    
    def get_task(self, task_id: str) -> TaskRecord | None:
        """Get a task by ID.
        
        Args:
            task_id: Unique task identifier.

        Returns:
            The task record if found, otherwise None.
        """
        return self.tasks.get(task_id)
    
    def claim_next_task(self) -> TaskRecord | None:
        """Claim the next pending task for a worker.
        
        Returns:
            The claimed task record, or None if no pending tasks exist.
        """
        if not self.pending_queue:
            return None
        
        task_id = self.pending_queue.popleft()
        task = self.tasks[task_id]
        task.status = TaskStatus.RUNNING

        return task
    
    def complete_task(
            self,
            task_id: str,
            request: TaskCompleteRequest,
    ) -> TaskRecord | None:
        """Mark a task as completed and store its result.
    
        Args:
            task_id: Unique task identifier.
            request: Worker request containing the task result.
        
        Returns:
            The updated task record if found, otherwise None.
        """
        task = self.tasks.get(task_id)

        if task is None:
            return None
        
        task.status = TaskStatus.COMPLETED
        task.result = request.result
        task.error = None

        return task
    
    def fail_task(
            self,
            task_id: str,
            request: TaskFailRequest,
    ) -> TaskRecord | None:
        """Mark a task as failed and store its error message.
        
        Args:
            task_id: Unique task identifier.
            request: Worker request containing the error message.

        Returns:
            The updated task record if found, otherwise None.
        """
        task = self.tasks.get(task_id)

        if task is None:
            return None
        
        task.status = TaskStatus.FAILED
        task.error = request.error

        return task