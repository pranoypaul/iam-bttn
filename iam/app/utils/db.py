"""Redis client class utility."""
import logging

# from redis import asyncio as aioredis
from iam.config import mongo as mongo_conf
from pymongo import MongoClient
from iam.app.exceptions import MONGO_CONNECTION_ERROR, DB_WRITE_ERROR, DB_READ_ERROR

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "salt": "dummy",
        "full_name": "John Doe",
        "secret_key": " ",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$xoFuX5rWW5yR3CkSnD6IgO8PT5gIKhzg.GvKrl25iwPxsJfTSDqJS",
        "disabled": False,
        "role": 0
    }
}



access_token_denylist = set()
refresh_token_denylist = set()
token_map = {}

class MongodbClient(object):
    """Define Redis utility.

    Utility class for handling Mongoi database connection and operations.



    """

    # redis_client: aioredis.Redis = None
    log: logging.Logger = logging.getLogger(__name__)
    mongo_connection_string: str = mongo_conf.MONGO_CONNECTION_STRING
    db_name = mongo_conf.DB_NAME

    @classmethod
    async def open_mongo_client(cls):
        """Create mongo client session object instance.

        Returns:
            MongoClient: MongoClient object instance.

        """
        cls.mongo_client: MongoClient = None
        
        if cls.mongo_client is None:
            cls.log.debug("Initializing Mongo client.")
            if cls.mongo_connection_string :
                try:
                    print(cls.mongo_connection_string)
                    cls.mongo_client =  MongoClient(cls.mongo_connection_string)
                    print(cls.mongo_client)
                    cls.db = cls.mongo_client[cls.db_name]
                    print("Connection to Mongo Successful")
                except Exception as e:
                    cls.log.exception(
                "Mongo connect command finished with exception",
                exc_info=(type(e), e, e.__traceback__),
                )
            else:
                print("Mongo connection string is None")
                return False
                
        return cls.mongo_client

    @classmethod
    async def close_mongo_client(cls):
        """Close mongo client."""
        if cls.mongo_client:
            cls.log.debug("Closing Mongo client")
            cls.mongo_client.close()

    @classmethod
    async def ping(cls):
        """Execute Mongo PING command.

        Ping the Mongo server.

        Returns:
            response: Boolean, whether Mongo client could ping Mongo server.

        Raises:
            Error: If Mongo client failed while executing ping.

        """
        # Note: Not sure if this shouldn't be deep copy instead?
        mongo_client = cls.mongo_client

        cls.log.debug("Execute Mongo PING command")
        try:
            return mongo_client[cls.db_name].command('ping')
        except Exception as e:
            cls.log.exception(
                "Mongo PING command finished with exception",
                exc_info=(type(e), e, e.__traceback__),
            )
            print(e)
            raise MONGO_CONNECTION_ERROR
    @classmethod
    async def insert(cls, collection: str, data: dict):
        col = cls.db[collection]
        try:
            col.insert_one(data)
        except Exception as e:
            cls.log.exception(
                    "Mongo insertion failed",
                    exc_info=(type(e), e, e.__traceback__),
                )
            raise DB_WRITE_ERROR
        
    @classmethod
    async def find_one(cls, collection: str, query: dict):
        col = cls.db[collection]
        try:
            return col.find(query)[0]
        except IndexError:
            return None
        except Exception as e:
            print(e)
            raise DB_READ_ERROR
    @classmethod
    async def find(cls, collection: str, query: dict):
        col = cls.db[collection]
        try:
            return col.find(query)
        except IndexError:
            return None
        except Exception as e:
            print(e)
            raise DB_READ_ERROR
    @classmethod
    async def query(cls, collection: str, query: dict ):
        db = cls.mongo_client[cls.db_name]
    @classmethod
    async def delete(cls, collection, ):
        db = cls.mongo_client[cls.db_name]
    @classmethod
    async def aggregate(cls, collection: str, pipeline: list):
        col = cls.db[collection]
        try:
            return col.aggregate(pipeline)
        except IndexError:
            return None
        except Exception as e:
            print(e)    
