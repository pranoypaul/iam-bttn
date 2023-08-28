from datetime import datetime, timedelta
import random, string

from bson.objectid import ObjectId
from jose import jwt
from typing import Optional
from iam.app.utils import MongodbClient, RedisClient
from iam.config import encryption, PEPPER, pwd_context
from iam.app.models import (UserInDB,
                            Action, User,
                            UserIn,
                            PermissionIn, 
                            PermissionOut,
                            RoleIn, RoleOut,
                            Application, 
                            Resource,
                            Permission,
                            UserOut,
                            )
from iam.app.utils.db import refresh_token_denylist, token_map 
from iam.app.helper_functions import (
    get_user,
    get_application,
    get_action, 
    get_password_hash,
    get_user_with_email,
    get_token_exp,
    get_resource,
    get_permission,
    get_all_resources,
    get_role,
    get_permission_by_id
    )

from iam.app.exceptions import (
    USER_ALREADY_EXISTS_ERROR,
    DB_WRITE_ERROR,
    ACTION_ALREADY_EXISTS_ERROR,
    EMAIL_ALREADY_EXISTS_ERROR,
    APPLICATON_ALREADY_EXISTS_ERROR,
    RESOURCE_ALREADY_EXISTS_ERROR,
    PERMISSION_ALREADY_EXISTS_ERROR,
    CUSTOM_HTTP_EXCEPTION,
    ROLE_ALREADY_EXISTS_ERROR
    )


"""-----------------------------------------------------------------"""
"""---------------------AUTHENTICATION-END--------------------------"""
"""-----------------------------------------------------------------"""

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)





async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    seasoned_password = user.salt+password+PEPPER

    if not verify_password(seasoned_password, user.hashed_password):
        return False
    return user
async def check_duplicate_name(username):
        user: User = await get_user(username=username)
        print("GOT user", user)
        if user is not None:
            print("User already exists")
            raise USER_ALREADY_EXISTS_ERROR
        
async def check_duplicate_email(email):
        user: User = await get_user_with_email(email=email)
        print("GOT user", user)
        if user is not None:
            print("User already exists")
            raise EMAIL_ALREADY_EXISTS_ERROR
        
async def check_duplicate(user: UserIn):
    
    await check_duplicate_name(user.username)
    await check_duplicate_email(user.email)

async def create_user(user_data: UserIn):
    
    #This check will raise an error is this is a duiplicate request
    await check_duplicate(user_data)
    disabled = False
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    hashed_password=get_password_hash(salt+user_data.secret_key+PEPPER)
    
    user_obj = UserInDB (
                    username=user_data.username,
                    hashed_password=hashed_password,
                    salt=salt,
                    email=user_data.email,
                    first_name=user_data.first_name,
                    middle_name=user_data.middle_name,
                    last_name=user_data.last_name,
                    roles=user_data.roles,
                    disabled=disabled,
                    created_at=datetime.now(),
                    created_by=None,
                    modified_at=datetime.now(),
                    modified_by=None
                    )
    user_dict = user_obj.dict()
    try:
        await MongodbClient.insert('User', user_dict)
        return await get_user(user_obj.username)
    
    except Exception as e:
        print(e)
        raise DB_WRITE_ERROR
                    
def set_refresh_token(username: str, refresh_token: str):
    #Need to check if exp is crossed
    if token_map.get(username, False):
        if token_map[username].get('refresh_token', False):
            refresh_token_denylist.add(token_map[username]['refresh_token'])
        token_map[username]["refresh_token"] =  refresh_token
    else:
        token_map[username] = {'refresh_token': refresh_token}

    
def set_access_token(username: str, access_token: str):
        if token_map.get(username, False):
            if token_map[username].get('access_token', False):
                refresh_token_denylist.add(token_map[username]['access_token'])
            token_map[username]["access_token"] =  access_token
        else:
            token_map[username] = {'access_token': access_token}
    
async def revoke_refresh_token(username: str):
    if token_map.get(username, False):
        if token_map[username].get('refresh_token', False):
            refresh_token = token_map[username]['refresh_token']
            token_exp = get_token_exp(token=refresh_token)
            print("token exppp", token_exp)
            exp_dtm = datetime.fromtimestamp(int(token_exp))
            print(exp_dtm)
            time_left  = exp_dtm - datetime.utcnow() 
            seconds_left = int(time_left.total_seconds())
            if  seconds_left < 0:
                print("Token alreay expired")
            else:
                await RedisClient.set(refresh_token, "revoked")
                await RedisClient.expire(refresh_token, seconds_left)
            

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        encryption.SECRET_KEY, 
        algorithm=encryption.ALGORITHM,
        headers={"kid": encryption.KID}
        )
    return encoded_jwt
"""-----------------------------------------------------------------"""
"""--------------------------ROLE-----------------------------------"""
"""-----------------------------------------------------------------"""


# Role CRUD operations
async def create_role(role: RoleIn) -> RoleOut:
    permissions = role.permissions
    permission_ids = []
    existing_role = await get_role(role.name)
    if existing_role:
        raise ROLE_ALREADY_EXISTS_ERROR
    for permission_name in permissions:
        permission_obj =  await get_permission(permission_name)
        if permission_obj:
            print(permission_obj)
            permission_ids.append(permission_obj.id)
            continue
        else:
            raise CUSTOM_HTTP_EXCEPTION(f"The permission {permission_name} does not exist")
    role.permissions = permission_ids
    print(role)
    await MongodbClient.insert('Role', role.dict())
    new_role = await get_role(role.name)
    print(new_role)
    return new_role

    
"""-----------------------------------------------------------------"""
"""--------------------------ACTION---------------------------------"""
"""-----------------------------------------------------------------"""
    

# Role CRUD operations
async def create_action(action: Action) -> Action:
    existing_action = await get_action(action.name)
    if not existing_action:
        new_action = action.dict()
        await MongodbClient.insert('Action', new_action)
        new_action = await get_action(action.name)
        return new_action
    else:
        raise ACTION_ALREADY_EXISTS_ERROR

"""-----------------------------------------------------------------"""
"""--------------------------APPLICATION----------------------------"""
"""-----------------------------------------------------------------"""
    

async def create_application(application: Application) -> Application:
    existing_application = await get_application(application.name)
    print(existing_application)
    if not existing_application:
        new_application = application.dict()
        await MongodbClient.insert('Application', new_application)
        new_application = await get_application(application.name)
        return new_application
    else:
        raise APPLICATON_ALREADY_EXISTS_ERROR
    
"""-----------------------------------------------------------------"""
"""--------------------------RESOURCE-------------------------------"""
"""-----------------------------------------------------------------"""
    
async def create_resource(resource: Resource) -> Resource:
    existing_resource = await get_resource(resource.name)
    print(existing_resource)
    if not existing_resource:
        new_resource = resource.dict()
        await MongodbClient.insert('Resource', new_resource)
        new_resource = await get_resource(resource.name)
        return new_resource
    else:
        raise RESOURCE_ALREADY_EXISTS_ERROR
    
"""-----------------------------------------------------------------"""
"""--------------------------PERMISSION-----------------------------"""
"""-----------------------------------------------------------------"""
    
async def create_permission(permission: Permission) -> Permission:
    existing_permission = await get_permission(permission.name)
    print(existing_permission)
    if not existing_permission:
        resources = permission.resource_actions.keys()
        valid_resources = set([resource.name for resource in await get_all_resources()])
        for resource in resources:
            if resource not in valid_resources:
                error_message = f"{resource} is not a valid resource"
                raise CUSTOM_HTTP_EXCEPTION(error_message)
        new_permission = permission.dict()
        await MongodbClient.insert('Permission', new_permission)
        new_permission = await get_permission(permission.name)
        return new_permission
    else:
        raise PERMISSION_ALREADY_EXISTS_ERROR