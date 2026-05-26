"""
FastAPI server for the AI Assistant
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config.settings import settings
from src.api.endpoints import router

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown"""
    logger.info("Starting AI Assistant API")
    logger.info(f"Model: {settings.MODEL_NAME}")
    yield
    logger.info("Shutting down AI Assistant API")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description="AI Assistant inspired by GitHub Copilot and ChatGPT",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(router)
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "model": settings.MODEL_NAME,
            "version": settings.API_VERSION
        }
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "name": settings.API_TITLE,
            "version": settings.API_VERSION,
            "docs": "/docs",
            "endpoints": {
                "health": "/health",
                "code_completion": "/api/complete",
                "chat": "/api/chat",
                "debug": "/api/debug",
                "explain": "/api/explain"
            }
        }
    
    # Error handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )
    
    logger.info("FastAPI application created successfully")
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower()
    )
