"""Application implementation - Auth controller."""
import logging
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from iam.config import settings, encryption
# from iam.app.utils import RedisClient
from iam.app.views import ReadyResponse, ErrorResponse
from iam.app.models import User, UserIn, Token, UserOut
from iam.app.exceptions import USER_DOESNT_EXIST_ERROR, TOKEN_INVALID_ERROR
from iam.app.helper_functions.response_helper import CustomJSONResponse
from iam.app.helper_functions import (
                                      create_user, 
                                      authenticate_user, 
                                      create_access_token, 
                                      set_refresh_token,
                                      set_access_token,
                                      )
from iam.app.helper_functions import (get_access_token_expiry,
                                      get_current_active_user,
                                      revoke_refresh_token,
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

@unauth_router.post("/create_token")
async def generate_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise USER_DOESNT_EXIST_ERROR
    
    access_token_expires = timedelta(minutes=encryption.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {
        'sub': user.username,
    }
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=encryption.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_access_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    set_refresh_token(username=user.username, refresh_token=refresh_token)
    set_access_token(username=user.username, access_token=access_token)
    response = {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    return CustomJSONResponse(status_code=201, message="User authenticated", content=response).response()

@unauth_router.post('/refresh_token')
def refresh(valid_user: User = Depends(get_current_active_user)):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    
    #Need to validate that this is the refresh token itself using
    # current_user = Authorize.get_jwt_subject()
    # new_access_token = Authorize.create_access_token(subject=current_user)
    
    access_token = create_access_token(
        data={"sub": valid_user.username}, expires_delta=timedelta(minutes=encryption.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/validate_token")
async def validate_access_token(
    valid_user: User = Depends(get_current_active_user)
    ):
    if not valid_user:
        raise TOKEN_INVALID_ERROR
    response = {"token_status": "Token is valid", "token_type": "bearer"}
    return CustomJSONResponse(status_Code=200, message="Token authenticated", content=response).response()

@router.post("/revoke_token")
async def revoke_refresh_access_token(
    valid_user: User = Depends(get_current_active_user)
    ):
    if not valid_user:
        raise TOKEN_INVALID_ERROR
    await revoke_refresh_token(valid_user.username)
    response = {"token_status": "Refresh token has been revoked"}
    
    return CustomJSONResponse(status_Code=200, message="Token authenticated", content=response).response()


@router.get("/users/me/")
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
    ):
    filtered_user = UserOut(**current_user.dict()).dict()
    return CustomJSONResponse(status_Code=200, content=filtered_user).response()


# @app.get("/customer/products", response_model=List[Product])
# def get_products_for_customer(user_id: int = Depends(has_permission(user_id=1, required_permission="view_product:product"))):
#     return products