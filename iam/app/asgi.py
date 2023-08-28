"""Application implementation - ASGI."""
import logging

from fastapi import FastAPI
from iam.config import settings
from iam.app.router import routes
from iam.app.utils import MongodbClient, RedisClient
from iam.app.exceptions import (
    HTTPException,
    http_exception_handler,
)
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


log = logging.getLogger(__name__)


async def on_startup():
    """Define FastAPI startup event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#startup-event

    """
    log.debug("Execute FastAPI startup event handler.")
    await MongodbClient.open_mongo_client()
    await RedisClient.open_redis_client()


async def on_shutdown():
    """Define FastAPI shutdown event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#shutdown-event

    """
    log.debug("Execute FastAPI shutdown event handler.")
    # Gracefully close utilities.

    await MongodbClient.close_mongo_client()


def get_application():
    """Initialize FastAPI application.

    Returns:
       FastAPI: Application object instance.

    """
    log.debug("Initialize FastAPI application node.")
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        docs_url=settings.DOCS_URL,
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
    )
    log.debug("Applying middlewares.")
    if not settings.DEBUG:
        #Only accept HTTPS requests
        app.add_middleware(HTTPSRedirectMiddleware)
        #CORS rules
        app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]
)
    #Adding middleware
    log.debug("Add application routes.")
    for route in routes:
        app.include_router(route)
    log.debug("Register global exception handler for custom HTTPException.")
    app.add_exception_handler(HTTPException, http_exception_handler)

    return app
