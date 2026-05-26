"""
API module - FastAPI endpoints and server
"""

from src.api.server import app, create_app
from src.api.endpoints import router

__all__ = ["app", "create_app", "router"]
