from pymongo import MongoClient

import utils # noqa


def create_connection(connect_string):
    """
    Create a MongoDB connection
    Args:
        connect_string (string): Connect string for DB
    Returns:
        client (MongoClient): MongoDB client object
    """
    client = MongoClient()
    client = MongoClient('mongodb://localhost:27017/')

    return client
