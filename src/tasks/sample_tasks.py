"""Sample task functions executed by workers.

This module contains simple task functions used to test the distributed task
queue. Each function can be called by name through the task registry.
"""

import time


def add(x: int | float, y: int | float) -> int | float:
    """Return the sum of two numbers.
    
    Args:
        x: First number.
        y: Second number.

    Returns:
        Sum of x and y.
    """
    return x + y


def reverse_text(text: str) -> str:
    """Return a reversed copy of a string.
    
    Args:
        text: Input text.
    
    Returns:
        Reversed text.
    """
    return text[::-1]


def sleep_task(seconds: int | float) -> str:
    """Sleep for a given number of seconds.
    
    Args:
        seconds: Number of seconds to sleep.

    Returns:
        Message confirming completion.
    """
    time.sleep(seconds)
    return f"Slept for {seconds} seconds."


def multiply(x: int | float, y: int | float) -> int | float:
    """Return the product of two numbers.
    
    Args:
        x: First number.
        y: Second number.
    
    Returns:
        Product of x and y.
    """
    return x * y