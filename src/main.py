"""Application entry point for the distributed task queue broker.

This module creates the FastAPI application instance and registers API routes.
"""

from fastapi import FastAPI

from src.api.routes_tasks import router as tasks_router


def create_app() -> FastAPI:
    """Creates and configure the FastAPI application.
    
    Returns:
        Configured FastAPI app instance.
    """
    app = FastAPI(
        title="Distributed Task Queue",
        description="A simple distributed task queue with broker, workers, and clients.",
        version="0.1.0",
    )

    app.include_router(tasks_router)

    return app


app = create_app()