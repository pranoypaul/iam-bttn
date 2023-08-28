from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    salt: Optional[str] = None
    hashed_password: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    secret_key: Optional[str] = None
    roles: Optional[List[str]] = []
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = None
    
class UserIn(BaseModel):
    username: str
    email: str 
    secret_key: str 
    phone_number: Optional[str] = None
    roles: Optional[List[str]] = [] 
    first_name: str
    middle_name: Optional[str] = None
    last_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: Optional[str] = None
    roles: Optional[List[str]] = []
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    roles: List[str]
    
class UserInDB(User):
    username: str
    salt: Optional[str] = None
    hashed_password: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    roles: Optional[List[str]] = []
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = None
    created_at: datetime
    created_by: Optional[str] = None
    modified_at: datetime
    modified_by: Optional[str] = None
    