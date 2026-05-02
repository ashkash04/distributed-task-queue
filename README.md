# distributed-task-queue

A distributed task queue built in Python with a FastAPI-based broker, worker processes, and client-side polling for asynchronous task execution.

This project demonstrates a basic distributed system where tasks are submitted by clients, stored and managed by a central broker, and executed by independent worker processes.

## Status

This project is currently a **MVP!**
Core task submission, execution, and result retrieval are implemented. More advanced distributed system features are planned.

## Features

- Submit tasks via HTTP API
- In-memory task storage in the broker
- Worker processes that poll and execute tasks
- Support for positional arguments
- Task lifecycle tracking:
  - pending -> running -> completed / failed
- Client-side polling for results

## Project Structure

```
src/
├── api/            # FastAPI routes
├── client/         # Task submission + polling
├── config.py       # Shared configuration
├── core/           # Task registry
├── main.py         # FastAPI app entry point
├── models/         # Pydantic models
├── storage/        # In-memory task store
├── tasks/          # Example task functions
└── worker/         # Worker process
```

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Requests
- Pydantic

## Quick Start

### 1. Start the broker

```powershell
uvicorn src.main:app --reload
```

### 2. Start a worker

```powershell
python -m src.worker.worker
```

### 3. Submit a task

```powershell
python -m src.client.client
```

## Notes

- Tasks are stored in memory (no persistence yet!)
- Broker is currently single-node (not replicated yet!)
- Workers use polling instead of push-based scheduling

## Future Improvements

- Persistent storage (SQLite / PostgreSQL)
- Multiple worker coordination and scaling
- Retry logic and task timeouts
- Worker heartbeats and failure detection
- Message queue integration (Redis / RabbitMQ)
- REST API improvements and CLI tools
- Dockerized deployment
- Observability (logging, metrics, tracing)
