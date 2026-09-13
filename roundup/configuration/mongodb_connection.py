import os
import sys

from roundup.exception import RoundupException
from roundup.constants import DATABASE_NAME, MONGODB_URL_KEY
from roundup.logger import logging

import pymongo
import certifi

ca = certifi.where()

class MongoDBClient:
    """
    MongoDB client for establishing and managing a connection
    to the application's MongoDB database.

    The client connection is initialized once and reused across
    instances of this class. The MongoDB connection URL is loaded
    from the environment using the configured environment variable.

    Attributes:
        client: Shared MongoDB client instance.
        database: MongoDB database instance.
        database_name: Name of the connected MongoDB database.

    Raises:
        RoundupException: If the MongoDB connection cannot be
        established or the required environment variable is missing.
    """

    client = None

    def __init__(self, database_name = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set!")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name

            logging.info("MongoDB connection succesfull")

        except Exception as e:
            raise RoundupException(e, sys)

