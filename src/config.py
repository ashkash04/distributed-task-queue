"""Project configuration constants.

This module stores shared configuration values for the broker, workers,
and client scripts.
"""

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 8000
BROKER_BASE_URL = f"http://{BROKER_HOST}:{BROKER_PORT}"

WORKER_POLL_INTERVAL_SECONDS = 1.0
WORKER_REQUEST_TIMEOUT_SECONDS = 5.0

DEFAULT_RETRY_LIMIT = 3