"""Application configuration - root APIRouter.

Defines all FastAPI application endpoints.

Resources:
    1. https://fastapi.tiangolo.com/tutorial/bigger-applications

"""
from fastapi import APIRouter
from iam.app.controllers import ready
from iam.app.controllers import auth
from iam.app.controllers import rbac

root_api_router = APIRouter(prefix="/iam")
auth_api_router = APIRouter(prefix="/iam/v1/auth")
unauth_api_router = APIRouter(prefix="/iam/v1/authpub")
rbac_api_router = APIRouter(prefix="/iam/v1/rbac")
rbac_pub_api_router = APIRouter(prefix="/iam/v1/rbacpub")

root_api_router.include_router(ready.router, tags=["ready"])
auth_api_router.include_router(auth.router, tags=["auth"])
unauth_api_router.include_router(auth.unauth_router, tags=["auth"])
rbac_api_router.include_router(rbac.router, tags=["rbac"])
rbac_pub_api_router.include_router(rbac.unauth_router, tags=["rbac"])

routes = [
    root_api_router,
    auth_api_router,
    unauth_api_router,
    rbac_api_router,
    rbac_pub_api_router,
]