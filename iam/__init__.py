"""Iam microservice."""
import logging

from iam.wsgi import ApplicationLoader
from iam.version import __version__

# initialize logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

__all__ = ("ApplicationLoader", "__version__")
