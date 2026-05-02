"""Task data models for the distributed task queue.

This module defines the core task-related data structures used by the broker,
client, and worker componenets. These models describe task creation requests,
stored task records, task status values, and task completion requests.
"""

from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Possible lifecycle states for a task."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskCreateRequest(BaseModel):
    """Request body used by a client to submit a new task.
    
    Attributes:
        name: Name of the task function to execute.
        args: Positional arguments passed to the task function.
    """

    name: str
    args: list[Any] = Field(default_factory=list)


class TaskRecord(BaseModel):
    """Internal task record stored by the broker.
    
    Attributes:
        id: Unique task identifier.
        name: Name of the task function to execute.
        args: Positional arguments for the task function.
        status: Current task lifecycle status.
        result: Task result after successful execution.
        error: Error message if the task failed.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    args: list[Any] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Any | None = None
    error: str | None = None


class TaskCompleteRequest(BaseModel):
    """Request body used by a worker to report task completion.
    
    Attributes:
        result: Result produced by the task.
    """

    result: Any | None = None


class TaskFailRequest(BaseModel):
    """Request body used by a worker to report task failure.
    
    Attributes:
        error: Error message describing why the task failed.
    """

    error: str