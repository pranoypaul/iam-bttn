"""Application implementation - Ready controller."""
import logging

from fastapi import APIRouter
from iam.config import settings
from iam.app.utils import MongodbClient, RedisClient
from iam.app.views import ReadyResponse, ErrorResponse
from iam.app.exceptions import HTTPException
from iam.app.helper_functions import CustomJSONResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.get(
    "/health",
    tags=["ready"],
    response_model=ReadyResponse,
    summary="Healthcheck route.",
    status_code=200,
    responses={502: {"model": ErrorResponse}},
)
async def readiness_check():
    """Run basic application health check.

    If the application is up and running then this endpoint will return simple
    response with status ok. Moreover, if it has Redis enabled then connection
    to it will be tested. If Redis ping fails, then this endpoint will return
    502 HTTP error.
    \f

    Returns:
        response (ReadyResponse): ReadyResponse model object instance.

    Raises:
        HTTPException: If applications has enabled Redis and can not connect
            to it. NOTE! This is the custom exception, not to be mistaken with
            FastAPI.HTTPException class.

    """
    log.info("Started GET /healthy")
    response = {
        'app': True,
        'database': True,
        'redis': True
    }
    if not await MongodbClient.ping():
        log.error("Could not connect to Mongo")
        raise HTTPException(
            status_code=502,
            content=ErrorResponse(
                code=502, message="Could not connect to Mongo"
            ).dict(exclude_none=True),
        )
    if not await RedisClient.ping():
        log.error("Could not connect to Redis")
        raise HTTPException(
            status_code=502,
            content=ErrorResponse(
                code=502, message="Could not connect to Redis"
            ).dict(exclude_none=True),
        )

    return CustomJSONResponse(status_code=200, message="Healthcheck success", content=response).response()

##Add health check for mogndb and the app as such

