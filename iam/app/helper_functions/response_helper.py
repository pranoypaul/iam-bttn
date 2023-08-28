"""Application implementation - custom FastAPI HTTP exception with handler."""
from typing import Any, Optional, Dict
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import TypeVar, Generic, Any, Union
from fastapi import Request
from fastapi.responses import JSONResponse


class CustomJSONResponse():
    
    def __init__(self, status_code: int, content: dict,message: int = ""):
        
        self.status_code = status_code
        self.content = content
        self.message = message
    def response(self):
        if self.status_code >=200 and self.status_code < 300:
            status = True
        else:
            status = False
        template_dict = {
            "status": status,
            "message": self.message,
            "data": self.content
        }
        return JSONResponse(
                    status_code=self.status_code,
                    content=template_dict
                )
        

