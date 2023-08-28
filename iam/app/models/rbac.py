import pydantic
from pydantic import BaseModel, Field 
from typing import Optional, List, Dict, Union
from bson import ObjectId


pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise ValueError("Not a valid ObjectId")
        return ObjectId(v)


class Action(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None


class Application(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None
    
    
class Resource(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None

class ResourceActionItem(BaseModel):
    type: str = "allow"
    actions: Union[str, List[str]]


class Permission(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None
    resource_actions: Dict[str, List[ResourceActionItem]]
    
class PermissionIn(BaseModel):
    name: str
    description: Optional[str] = None
    resource_actions: Dict[str, List[ResourceActionItem]]


class PermissionOut(PermissionIn):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

class Role(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    permissions: List[str]

class RoleIn(BaseModel):
    name: str
    description: str
    permissions: Union[List[PyObjectId], List[str]]


class RoleOut(RoleIn):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    permissions: List[Permission]