"""
Main entry point for the AI Assistant application
"""

import os
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
from src.api.server import app
from src.config.settings import settings

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point"""
    logger.info("Starting AI Assistant")
    logger.info(f"Configuration:")
    logger.info(f"  - Model: {settings.MODEL_NAME}")
    logger.info(f"  - Host: {settings.API_HOST}:{settings.API_PORT}")
    logger.info(f"  - Debug: {settings.DEBUG}")
    logger.info(f"  - Workers: {settings.WORKERS}")
    
    # Create logs directory if it doesn't exist
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Start the server
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    main()
