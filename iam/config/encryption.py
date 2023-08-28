from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# to get a string like this run:
# openssl rand -hex 32
from pydantic import BaseSettings
class Encryption(BaseSettings):
    
    
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30
    KID: str = "HPe09PmpyBXllhEXRSbjOI8ZfePI7Myy"
    class Config:
        """Config sub-class needed to customize BaseSettings settings. """

        case_sensitive = True
        env_prefix = "AUTH_"
        
PEPPER = "TCsrq6zQEqrNhIBt"

encryption = Encryption()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

