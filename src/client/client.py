"""Example client for submitting tasks to the broker.

This module provides small helper functions for submitting tasks and checking
task status through the broker's HTTP API.
"""

import time
from typing import Any

import requests

from src.config import BROKER_BASE_URL, WORKER_REQUEST_TIMEOUT_SECONDS
from src.models.task import TaskCreateRequest, TaskRecord, TaskStatus


def submit_task(
        name: str,
        args: list[Any] | None = None,
) -> TaskRecord:
    """Submit a task to the broker.
    
    Args:
        name: Name of the registered task function to execute.
        args: Positional arguments for the task function.
    
    Returns:
        The created task record returned by the broker.
    """
    request = TaskCreateRequest(
        name=name,
        args=args or [],
    )

    response = requests.post(
        f"{BROKER_BASE_URL}/tasks/",
        json=request.model_dump(),
        timeout=WORKER_REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    return TaskRecord.model_validate(response.json())


def get_task(task_id: str) -> TaskRecord:
    """Fetch a task record from the broker.
    
    Args:
        task_id: Unique task identifier.
    
    Returns:
        The task record returned by the broker.
    """
    response = requests.get(
        f"{BROKER_BASE_URL}/tasks/{task_id}",
        timeout=WORKER_REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    return TaskRecord.model_validate(response.json())


def wait_for_result(
        task_id: str,
        poll_interval_seconds: float = 0.5,
) -> TaskRecord:
    """Poll the broker until a task completes or fails."""
    while True:
        task = get_task(task_id)

        if task.status in {TaskStatus.COMPLETED, TaskStatus.FAILED}:
            return task
        
        time.sleep(poll_interval_seconds)


def main() -> None:
    """Submit an example task and print the created task record."""
    task = submit_task("add", args=[2, 3])
    print("Submitted task:")
    print(task.model_dump())

    completed_task = wait_for_result(task.id)

    if completed_task.status == TaskStatus.COMPLETED:
        print(f"Result: {completed_task.result}")
    else:
        print(f"Task failed: {completed_task.error}")


if __name__ == "__main__":
    main()