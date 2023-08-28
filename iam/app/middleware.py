from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware import Middleware
from iam.config import encryption
from pydantic import BaseModel
from typing import Dict, List
import jwt

class AccessControlMiddleware:
    async def __call__(self, request: Request, call_next):
        # Get the JWT token from the request headers
        auth_header = request.headers.get("Authorization")

        if not auth_header or "Bearer" not in auth_header:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = auth_header.split(" ")[1]

        try:
            # Decode the JWT token to obtain user's role(s) and permissions
            payload = jwt.decode(token, encryption.SECRET_KEY, algorithms=[encryption.ALGORITHM])

            # Check if the user has access to the current application
            app_name = "iam"  # Replace with the application name you want to check
            if not payload["permissions"].get(app_name):
                raise HTTPException(status_code=403, detail="Forbidden: No access to the application")
            
        except Exception as e:
            print(e)