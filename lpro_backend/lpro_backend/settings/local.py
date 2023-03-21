import os

from .base import *

MIDDLEWARE += [
    "silk.middleware.SilkyMiddleware",
]
INSTALLED_APPS += [
    "silk",
]
SILK_ENABLED = True


FIXTURE_DIRS = ["/calculator/fixtures"]
