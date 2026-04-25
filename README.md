# distributed-task-queue

A simple distributed task queue built in Python.

This project will implement a central broker, task-submitting clients, and worker processes that pull takss from the broker, execute them, and return results.

## Planned Features

- Submit tasks through a client
- Store pending, running, and completed tasks in a broker
- Run multiple worker processes
- Execute registereed Python task functions
- Track task status and results
- Add retry logic and basic fault tolerance later

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Requests
- Pydantic