"""Task API routes for the broker.

This module defines HTTP endpoints for submitting tasks, claiming tasks,
checking task status, and reporting task completion or failure.
"""

from fastapi import APIRouter, HTTPException

from src.models.task import (
    TaskCompleteRequest,
    TaskCreateRequest,
    TaskFailRequest,
    TaskRecord,
)
from src.storage.memory_store import MemoryTaskStore

router = APIRouter(prefix="/tasks", tags=["tasks"])
store = MemoryTaskStore()


@router.post("/", response_model=TaskRecord)
def submit_task(request: TaskCreateRequest) -> TaskRecord:
    """Submit a new task to the broker.
    
    Args:
        request: Task creation request from a client.
    
    Returns:
        The created task record.
    """
    return store.create_task(request)


@router.get("/{task_id}", response_model=TaskRecord)
def get_task(task_id: str) -> TaskRecord:
    """Get a task by its ID.
    
    Args:
        task_id: Unique task identifier.
    
    Returns:
        The matching task record.
    
    Raises:
        HTTPException: If no task exists with the given ID.
    """
    task = store.get_task(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    return task


@router.post("/claim", response_model=TaskRecord | None)
def claim_task() -> TaskRecord | None:
    """Claim the next pending task for a worker.
    
    Returns:
        The next pending task if one exists, otherwise None.
    """
    return store.claim_next_task()


@router.post("/{task_id}/complete", response_model=TaskRecord)
def complete_task(task_id: str, request: TaskCompleteRequest) -> TaskRecord:
    """Mark a task as completed.
    
    Args:
        task_id: Unique task identifier.
        request: Request body containing the task result.
    
    Returns:
        The updated task record.

    Raises:
        HTTPException: If no task exists with the given ID.
    """
    task = store.complete_task(task_id, request)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    return task


@router.post("/{task_id}/fail", response_model=TaskRecord)
def fail_task(task_id: str, request: TaskFailRequest) -> TaskRecord:
    """Mark a task as failed.
    
    Args:
        task_id: Unique task identifier.
        request: Request body containing the error message.

    Returns:
        The updated task record.

    Raises:
        HTTPException: If no task exists with the given ID.
    """
    task = store.fail_task(task_id, request)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    return task