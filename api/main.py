from contextlib import asynccontextmanager
from loguru import logger
from fastapi import FastAPI
from .routes import router
from .database import create_db_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup: Creating database tables if they don't exist...")
    try:
        create_db_tables()
        logger.info("Database tables checked/created successfully.")
    except Exception as err:
        logger.error(f"Failed to create database tables: {err}")
        raise
    
    yield
    
    logger.info("Application shutdown: Cleaning up resources...")

app = FastAPI(lifespan=lifespan)

app.include_router(router)

logger.remove()

logger.add("./api/logs/dev_api.log",
          rotation="10 MB",
          retention="7 days",
          compression="zip",
          level="TRACE",
          enqueue=True,
          format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")