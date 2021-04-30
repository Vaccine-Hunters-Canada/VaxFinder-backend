from typing import List
import os
import logging
import time
import argparse

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger as fastapi_logger
from loguru import logger

from api import logging_config

from api import env_variables
from api.routers import entries, locations, organizations, addresses

from api.database.database import MSSQLBackend

from sqlalchemy import dialects

app = FastAPI(title='VaxFinder Backend')
fastapi_logger = logging_config.make_logger()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--database_url', type=str,
                    help='The database URL')
args = parser.parse_args()
os.environ['DATABASE_URL'] = args.database_url

@app.on_event("startup")
async def startup() -> None:
    # check enviroment variables
    env_variables.check_and_make()

    # ####################################################### #
    #               Database startup procedure                #
    # ####################################################### #
    db = MSSQLBackend(os.environ['DATABASE_URL'])

    while True:
        try:
            # check health
            connection = await db.connect()
            logger.info('Database connection established')
            await db.disconnect()
            break
        except Exception as e:
            logger.critical(e)
            logger.critical('Connecting to database...')
            time.sleep(5)

app.include_router(
    entries.router,
    prefix='/api/v1/entries',
    tags=['Entries'],
)

app.include_router(
    locations.router,
    prefix='/api/v1/locations',
    tags=['Locations'],
)

app.include_router(
    organizations.router,
    prefix='/api/v1/organizations',
    tags=['Organizations'],
)

app.include_router(
    addresses.router,
    prefix='/api/v1/addresses',
    tags=['Addresses'],
)

if __name__ == "__main__":
    uvicorn.run("api.main:app", port=8007, log_level="info", reload=True)
