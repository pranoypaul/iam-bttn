"""Application configuration - Mongo."""
from pydantic import BaseSettings

class Mongo(BaseSettings):
    """Define Mongo configuration model.

    Constructor will attempt to fetch the values of the following fields from
    env variables, if not present it will use the default values. The env variable 
    should have a prefix FASTAPI_ for this to work. This prefix can be adjusted in the 
    Config class below

    Environment variables:
        * FASTAPI_MONGO_CONNECTION_STRING
        * FASTAPI_DB_NAME

    Attributes:
        MONGO_CONNECTION_STRING (str): Connection string for mongo.
    """
    
    MONGO_CONNECTION_STRING: str = "mongodb://app_user:app_password@localhost:27017"
    DB_NAME: str = "Authentication"

    class Config:
        case_sensitive = True
        env_prefix = "FASTAPI_"


mongo = Mongo()

#Add more metadata in the jwt token
#Share encruption key betweeen api gateway
