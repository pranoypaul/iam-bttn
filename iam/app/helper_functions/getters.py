
from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt
from typing import Optional, List
from bson.objectid import ObjectId
from iam.config import encryption, pwd_context, oauth2_scheme
from iam.app.utils.db import access_token_denylist, refresh_token_denylist
from iam.app.models import (
    TokenData, 
    User, 
    UserOut, 
    Action, 
    Application,
    Resource,
    Permission,
    Role,
    RoleOut,
    )
from iam.app.exceptions import (
    USER_ALREADY_EXISTS_ERROR,
    DB_WRITE_ERROR,
    TOKEN_INVALID_ERROR,
    TOKEN_EXPIRED_ERROR,
    USER_DISABLED_ERROR,
    TOKEN_ACCESS_REVOKED,
    )

from iam.app.utils import MongodbClient, RedisClient


"""-------------------------------------------------------------"""
"""---------------------AUTHENTICATION--------------------------"""
"""-------------------------------------------------------------"""

def get_access_token_expiry():
    return encryption.ACCESS_TOKEN_EXPIRE_MINUTES

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_all_users():
    query = {}
    users =  await MongodbClient.find('User', query)
    user_list = []
    for user in users:
        user_list.append(UserOut(**user).dict())
    return user_list

async def get_user(username: str):
    query = { "username": username }
    user_dict =  await MongodbClient.find_one('User', query)
    if user_dict:
        user = User (
                    username=user_dict['username'],
                    hashed_password=user_dict['hashed_password'],
                    salt=user_dict['salt'],
                    email=user_dict['email'],
                    first_name=user_dict['first_name'],
                    last_name=user_dict['last_name'],
                    middle_name=user_dict['middle_name'],
                    roles=user_dict['roles'],
                    disabled=user_dict['disabled']
                    )
        return user
    return None
    
def get_token_exp(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, encryption.SECRET_KEY, algorithms=[encryption.ALGORITHM])
        expiry: int = payload.get("exp")
        print("Expity of token issss")
        return expiry
    except JWTError:
        raise TOKEN_INVALID_ERROR
    except jwt.ExpiredSignature:
        raise TOKEN_EXPIRED_ERROR
        

async def check_refresh_token_revoke_status(token: str):

    value = await RedisClient.get(token)
    if value:
            raise TOKEN_ACCESS_REVOKED
    return True





"""-----------------------------------------------------------------"""
"""---------------------AUTHENTICATION-END--------------------------"""
"""-----------------------------------------------------------------"""

async def get_current_user(token: str = Depends(oauth2_scheme)):
    
    is_active = await check_refresh_token_revoke_status(token)
    if is_active:
        try:
            payload = jwt.decode(token, encryption.SECRET_KEY, algorithms=[encryption.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise TOKEN_INVALID_ERROR
            token_data = TokenData(username=username)
        
        except JWTError:
            raise TOKEN_INVALID_ERROR
        except jwt.ExpiredSignature:
            raise TOKEN_EXPIRED_ERROR
        user = await get_user(username=token_data.username)
        if user is None:
            raise TOKEN_INVALID_ERROR
        return user
    
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise USER_DISABLED_ERROR
    return current_user

async def get_user_with_email(email: str):
        # user_dict = db[username]
    myquery = { "email": email }
    user_dict =  await MongodbClient.find_one('User', myquery)
    if user_dict:
        user = User (
                    username=user_dict['username'],
                    hashed_password=user_dict['hashed_password'],
                    salt=user_dict['salt'],
                    email=user_dict['email'],
                    full_name=user_dict['full_name'],
                    role=user_dict['role'],
                    disabled=user_dict['disabled']
                    )
        return user
    return None




def get_all_roles():
    pass


"""-----------------------------------------------------------------"""
"""---------------------ACTIONS-------------------------------------"""
"""-----------------------------------------------------------------"""

async def get_action(action_name: str):
    query = { "name": action_name }
    action_dict =  await MongodbClient.find_one('Action', query)
    if action_dict:
        action = Action(**action_dict)
        return action
    return None

async def get_all_actions():
    query = {}
    action_list =  await MongodbClient.find('Action', query)
    if action_list:
        actions = [Action(**action) for action in action_list]
        return actions
    return None
"""-----------------------------------------------------------------"""
"""---------------------APPLICATION---------------------------------"""
"""-----------------------------------------------------------------"""

async def get_application(action_name: str):
    query = { "name": action_name }
    action_dict =  await MongodbClient.find_one('Application', query)
    print(action_dict)
    if action_dict:
        action = Application(**action_dict)
        return action
    return None

async def get_all_applications():
    query = {}
    action_list =  await MongodbClient.find('Application', query)
    if action_list:
        actions = [Application(**action) for action in action_list]
        return actions
    return None


"""-----------------------------------------------------------------"""
"""---------------------RESOURCE------------------------------------"""
"""-----------------------------------------------------------------"""

async def get_resource(resource_name: str):
    query = { "name": resource_name }
    resource_dict =  await MongodbClient.find_one('Resource', query)
    if resource_dict:
        resource = Resource(**resource_dict)
        return resource
    return None

async def get_all_resources():
    query = {}
    resource_list =  await MongodbClient.find('Resource', query)
    if resource_list:
        resources = [Resource(**resource) for resource in resource_list]
        return resources
    return None


"""-----------------------------------------------------------------"""
"""---------------------PERMISSION----------------------------------"""
"""-----------------------------------------------------------------"""

async def get_permission(permission_name: str):
    query = { "name": permission_name }
    permission_dict =  await MongodbClient.find_one('Permission', query)
    if permission_dict:
        permission = Permission(**permission_dict)
        return permission
    return None
async def get_permission_by_id(permission_id: str):
    query = { "_id": ObjectId(permission_id) }
    permission_dict =  await MongodbClient.find_one('Permission', query)
    if permission_dict:
        permission = Permission(**permission_dict)
        return permission
    return None

async def get_all_permissions():
    query = {}
    permission_list =  await MongodbClient.find('Permission', query)
    if permission_list:
        permissions = [Permission(**permission) for permission in permission_list]
        return permissions
    return None

"""-----------------------------------------------------------------"""
"""---------------------ROLE----------------------------------------"""
"""-----------------------------------------------------------------"""

async def get_role(role_name: str):
    pipeline = [
            {
                '$match': {
                    'name': role_name
                }
            },
            {
                '$unwind': {
                    'path': '$permissions'
                }
            },
                {
                '$lookup': {
                    'from': 'Permission',
                    'localField': 'permissions',
                    'foreignField': '_id',
                    'as': 'permission_documents'
                }
            },
            {
                '$unwind': {
                    'path': '$permission_documents'
                }
            },
                {
                '$group': {
                    '_id': '$_id',
                    'permissions': {'$push': '$permission_documents'},
                    # Add any other fields from the Role collection you want to preserve in the output
                    'name': {'$first': '$name'},
                    'description': {'$first': '$description'},
                    # ...
                }
            }
        ]
    role_list = list(await MongodbClient.aggregate('Role', pipeline))
    if role_list:
        role_dict =  role_list[0]
        if role_dict:
            print(role_dict)
            print("zzzzz")
            role = RoleOut(**role_dict)
            return role
    return None


async def get_all_roles():
    pipeline = [            
            {
                '$unwind': {
                    'path': '$permissions'
                }
            },
                {
                '$lookup': {
                    'from': 'Permission',
                    'localField': 'permissions',
                    'foreignField': '_id',
                    'as': 'permission_documents'
                }
            },
            {
                '$unwind': {
                    'path': '$permission_documents'
                }
            },
                {
                '$group': {
                    '_id': '$_id',
                    'permissions': {'$push': '$permission_documents'},
                    # Add any other fields from the Role collection you want to preserve in the output
                    'name': {'$first': '$name'},
                    'description': {'$first': '$description'},
                    # ...
                }
            }
        ]
    role_list =  await MongodbClient.aggregate('Role', pipeline)
    if role_list:
        role = [RoleOut(**role) for role in role_list]
        return role
    return None