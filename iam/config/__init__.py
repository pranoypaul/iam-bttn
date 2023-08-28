"""Application configuration.

The ``config`` submodule defines configuration for your application, router,
gunicorn, and more.

Resources:
    1. `Pydantic documentation`_
    2. `Gunicorn documentation`_

.. _Pydantic documentation:
    https://pydantic-docs.helpmanual.io/

.. _Gunicorn documentation:
    https://docs.gunicorn.org/en/20.1.0/

"""
from iam.config.application import settings
from iam.config.redis import redis
from iam.config.mongodb import mongo
from iam.config.encryption import (
    encryption,
    pwd_context, 
    oauth2_scheme,
    PEPPER,
    )




__all__ = (
    "settings",
    "redis",
    "encryption",
    "pwd_context",
    "oauth2_scheme",
    "PEPPER",
    "mongo",
    )
