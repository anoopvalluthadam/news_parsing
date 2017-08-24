import os
import sys
import inspect
import pytest
import asyncio
import aioredis

currentdir = os.path.dirname(os.path.abspath(
                             inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import utils # noqa
from db.np_mongodb import NPMongoDB # noqa


@pytest.fixture(scope="module")
def connect_string():
    """
    Generate connect_string for MongoDB
    """
    config = utils.read_from_configuration('../config.yaml')
    connect_string = utils.get_db_connect_string(config)

    return connect_string


@pytest.fixture(scope="module")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="module")
def db(connect_string):
    db = NPMongoDB(connect_string)
    return db


@pytest.fixture(scope="module")
async def queue():
    redis = await aioredis.create_redis(('localhost', 6379))
    return redis
