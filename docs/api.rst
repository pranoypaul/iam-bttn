:tocdepth: 2
API
===

This part of the documentation lists the full API reference of all classes and functions.

WSGI
----

.. autoclass:: iam.wsgi.ApplicationLoader
   :members:
   :show-inheritance:

Config
------

.. automodule:: iam.config

.. autoclass:: iam.config.application.Application
   :members:
   :show-inheritance:

.. autoclass:: iam.config.redis.Redis
   :members:
   :show-inheritance:

.. automodule:: iam.config.gunicorn

CLI
---

.. automodule:: iam.cli

.. autofunction:: iam.cli.cli.cli

.. autofunction:: iam.cli.utils.validate_directory

.. autofunction:: iam.cli.serve.serve

App
---

.. automodule:: iam.app

.. autofunction:: iam.app.asgi.on_startup

.. autofunction:: iam.app.asgi.on_shutdown

.. autofunction:: iam.app.asgi.get_application

.. automodule:: iam.app.router

Controllers
~~~~~~~~~~~

.. automodule:: iam.app.controllers

.. autofunction:: iam.app.controllers.ready.readiness_check

Models
~~~~~~

.. automodule:: iam.app.models

Views
~~~~~

.. automodule:: iam.app.views

.. autoclass:: iam.app.views.error.ErrorModel
   :members:
   :show-inheritance:

.. autoclass:: iam.app.views.error.ErrorResponse
   :members:
   :show-inheritance:

Exceptions
~~~~~~~~~~

.. automodule:: iam.app.exceptions

.. autoclass:: iam.app.exceptions.http.HTTPException
   :members:
   :show-inheritance:

.. autofunction:: iam.app.exceptions.http.http_exception_handler

Utils
~~~~~

.. automodule:: iam.app.utils

.. autoclass:: iam.app.utils.aiohttp_client.AiohttpClient
   :members:
   :show-inheritance:

.. autoclass:: iam.app.utils.redis.RedisClient
   :members:
   :show-inheritance:
