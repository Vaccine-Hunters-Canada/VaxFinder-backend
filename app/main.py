import time
from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app import logging_config
from app.api.api_v1.api import api_router
from app.api.openapi_tags import openapi_tags
from app.core.config import settings
from app.db.database import MSSQLBackend

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    openapi_url=settings.OPENAPI_URL,
    docs_url=settings.SWAGGER_URL,
    redoc_url=settings.REDOC_URL,
    openapi_tags=openapi_tags,
)

fastapi_logger = logging_config.make_logger()

# --- Cross-Origin Resource Sharing ---
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Startup Procedure ---
@app.on_event("startup")
async def startup() -> None:
    db = MSSQLBackend(settings.DB_URL)

    while True:
        try:
            # check health
            await db.connect()
            logger.info("Database connection established")
            await db.disconnect()
            break
        except Exception as e:
            logger.critical(e)
            logger.critical("Connecting to database...")
            time.sleep(5)


# --- Routes ---
app.include_router(
    api_router, prefix=settings.API_V1_STR, include_in_schema=True
)

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8007, log_level="info", reload=True)
