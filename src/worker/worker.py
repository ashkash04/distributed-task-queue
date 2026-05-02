"""Worker process for executing tasks from the broker.

This module runs a polling worker that repeatedly asks the broker for pending
tasks, executes registered task functions, and reports success or failure.
"""

import time
from typing import Any

import requests

from src.config import BROKER_BASE_URL, WORKER_POLL_INTERVAL_SECONDS, WORKER_REQUEST_TIMEOUT_SECONDS
from src.core.task_registry import get_task_function
from src.models.task import TaskRecord


def claim_task() -> dict[str, Any] | None:
    """Claims the next pending task from the broker.
    
    Returns:
        Task data if a pending task is available, otherwise None.
    """
    response = requests.post(
        f"{BROKER_BASE_URL}/tasks/claim",
        timeout=WORKER_REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    data = response.json()

    if data is None:
        return None

    return TaskRecord.model_validate(data)


def report_task_success(task_id: str, result: Any) -> None:
    """Report successful task execution to the broker.
    
    Args:
        task_id: ID of the completed task.
        result: Result produced by the task function.
    """
    response = requests.post(
        f"{BROKER_BASE_URL}/tasks/{task_id}/complete",
        json={"result": result},
        timeout=WORKER_REQUEST_TIMEOUT_SECONDS
    )
    response.raise_for_status()


def report_task_failure(task_id: str, error: str) -> None:
    """Report failed task execution to the broker.
    
    Args:
        task_id: ID of the failed task.
        error: Error message describing the failure.
    """
    response = requests.post(
        f"{BROKER_BASE_URL}/tasks/{task_id}/fail",
        json={"error": error},
        timeout=WORKER_REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()


def execute_task(task: TaskRecord) -> None:
    """Execute a claimed task and report he result to the broker.
    
    Args:
        task: Task record received from the broker.
    """
    task_id = task.id
    task_name = task.name
    args = task.args

    try:
        task_function = get_task_function(task_name)
        result = task_function(*args)
        report_task_success(task_id, result)
    
    except Exception as error:
        report_task_failure(task_id, str(error))


def run_worker() -> None:
    """Continuously poll the broker for tasks and execute them."""
    print("Worker started. Press Ctrl+C to stop.")

    while True:
        task = claim_task()

        if task is None:
            time.sleep(WORKER_POLL_INTERVAL_SECONDS)
            continue

        print(f"Claimed task {task.id} ({task.name})")
        execute_task(task)


if __name__ == "__main__":
    run_worker()