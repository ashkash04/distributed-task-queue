"""Task registry for mapping task names to Python functions.

This module defines which task functions workers are allowed to execute.
Workers receive a task name from the broker, look it up in this registry,
and then call the matching Python function.
"""

from collections.abc import Callable
from typing import Any

from src.tasks.sample_tasks import add, multiply, reverse_text, sleep_task


TASK_REGISTRY: dict[str, Callable[..., Any]] = {
    "add": add,
    "multiply": multiply,
    "reverse_text": reverse_text,
    "sleep": sleep_task,
}


def get_task_function(task_name: str) -> Callable[..., Any]:
    """Return the Python function registered for a task name.
    
    Args:
        task_name: Name of the task function to look up.
    
    Returns:
        The Python function associated with the task name.

    Raises:
        KeyError: If the task name is not registered.
    """
    return TASK_REGISTRY[task_name]