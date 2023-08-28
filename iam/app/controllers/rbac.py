"""Application implementation - Auth controller."""
import logging

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi import APIRouter, HTTPException, Depends
from typing import List


# from iam.app.utils import RedisClient
from iam.app.views import ReadyResponse, ErrorResponse
from iam.app.models import (
                                UserIn,
                                UserOut, 
                                Action, 
                                PermissionIn,
                                PermissionOut, 
                                RoleIn, 
                                RoleOut, 
                                Role,
                                Application,
                                Resource,
                                Permission
                            )
from iam.app.helper_functions.response_helper import CustomJSONResponse
from iam.app.helper_functions import (
                                      create_user, 
                                      create_permission, 
                                      create_role, 
                                      create_action,
                                      create_application,
                                      create_resource,
                                      )
from iam.app.helper_functions import (
                                      get_all_users,
                                      get_all_actions,
                                      get_all_permissions, 
                                      get_all_applications,
                                      get_all_resources,
                                      get_all_roles,
                                      )

router = APIRouter()
unauth_router = APIRouter()
log = logging.getLogger(__name__)
"""{
  "sub": "12345678-1234-5678-9abc-def123456789",
  "iss": "authentication_service",
  "aud": "ecommerce_app",
  "exp": 1677649420,
  "iat": 1677645820,
  "roles": ["admin"],
  "permissions": {
    "ecommerce": ["create_product", "edit_product", "delete_product"]
  }
}"""


@unauth_router.post("/create_user")
async def create_new_user(user_data: UserIn):
    new_user = await create_user(user_data)
    response = UserOut(**new_user.dict()).dict()
    return CustomJSONResponse(status_code=201, message="User created successfully", content=response).response()

@router.get("/users")
async def edit_role():
    users = await get_all_users()
    print(users)
    return CustomJSONResponse(status_code=200, message="User created successfully", content=users).response()






# @router.put("/roles/{role_id}", response_model=RoleOut)
# async def update_existing_role(role_id: str, role: RoleIn, user: UserOut):
#     role = update_role(role_id, role, user)
#     if role is None:
#         raise HTTPException(status_code=404, detail="Role not found")
#     return role


# @router.delete("/roles/{role_id}", status_code=204)
# async def delete_existing_role(role_id: str, user: UserOut):
#     deleted = delete_role(role_id, user)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Role not found")
    

# Action endpoints
@router.post("/create_action", response_model=Action, status_code=201)
async def create_new_action(action: Action):
    action = await create_action(action)
    return action
@router.get("/actions", response_model=List[Action])
async def list_actions():
    actions = await get_all_actions()
    # response = ResponseWrapper[List[Action]](status=True, message="Data retrieved successfully", data=actions)
    # print(response)
    return actions


# Application endpoints
@router.post("/create_application", response_model=Application, status_code=201)
async def create_new_application(application: Application):
    action = await create_application(application)
    return action

@router.get("/applications", response_model=List[Application])
async def list_applications():
    applications = await get_all_applications()
    print(applications)
    return applications

# Resource endpoints
@router.post("/create_resource", response_model=Resource, status_code=201)
async def create_new_resource(application: Resource):
    action = await create_resource(application)
    return action

@router.get("/resources", response_model=List[Resource])
async def list_resources():
    applications = await get_all_resources()
    return applications

# Permission endpoints
@router.post("/create_permission", response_model=Permission, status_code=201)
async def create_new_permission(application: Permission):
    action = await create_permission(application)
    return action

@router.get("/permissions", response_model=List[Permission])
async def list_permissions():
    permissions = await get_all_permissions()
    return permissions

# Role endpoints
@router.post("/create_role", response_model=RoleOut, status_code=201)
async def create_new_role(role: RoleIn):
    role = await create_role(role)
    return role


@router.get("/roles/{role_id}", response_model=RoleOut)
async def get_role(role_id: str, user: UserOut):
    role = get_role_by_id(role_id, user)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.get("/roles", response_model=List[RoleOut])
async def list_roles():
    roles = await get_all_roles()
    return roles