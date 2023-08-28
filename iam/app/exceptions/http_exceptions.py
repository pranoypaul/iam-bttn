from iam.app.exceptions import HTTPException
from fastapi import status


def CUSTOM_HTTP_EXCEPTION(message: str):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": False,
            "message": message
        }
    )

USER_DOESNT_EXIST_ERROR = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": False,
                "message": "User does not exist"
            }
        )
EMAIL_ALREADY_EXISTS_ERROR = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": False,
                "message": "Email already exists"
            }
        )

TOKEN_ACCESS_REVOKED = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": False,
                "message": "The access of this token has been revoked"
            }
        )
USER_ALREADY_EXISTS_ERROR = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": False,
                "message": "User already exists"
            }
        )
DB_WRITE_ERROR = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": False,
                "message": "The data couldnt be written to database"
            }
        )
DB_READ_ERROR = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": False,
                "message": "The data couldnt be read from database"
            }
        )
MONGO_CONNECTION_ERROR = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": False,
                "message": "Could not connect to the database"
            }
        )
TOKEN_INVALID_ERROR = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": False,
                "message": "The JWT token given is invalid"
            }
        )

TOKEN_EXPIRED_ERROR = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": False,
                "message": "The JWT token given is invalid or expired"
            }
        )
USER_DISABLED_ERROR = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": False,
                "message": "The Given user is disabled"
            }
        )
ACTION_ALREADY_EXISTS_ERROR = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": False,
                "message": "Action already exists"
            }
        )

APPLICATON_ALREADY_EXISTS_ERROR = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": False,
                "message": "Application already exists"
            }
        )
RESOURCE_ALREADY_EXISTS_ERROR=HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": False,
                "message": "Resource already exists"
            }
        )
PERMISSION_ALREADY_EXISTS_ERROR=HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": False,
                "message": "Permission already exists"
            }
        )
ROLE_ALREADY_EXISTS_ERROR=HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": False,
                "message": "Role already exists"
            }
        )