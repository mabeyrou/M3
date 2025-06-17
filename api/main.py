from loguru import logger
from fastapi import FastAPI
from .routes import router

app = FastAPI()
app.include_router(router)

logger.remove()

logger.add("./api/logs/dev_api.log",
          rotation="10 MB",
          retention="7 days",
          compression="zip",
          level="TRACE",
          enqueue=True,
          format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")