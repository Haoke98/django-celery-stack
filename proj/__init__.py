import logging
import os
import platform

from django.conf.global_settings import DEBUG

from .celery import app as celery_app

__all__ = ('celery_app',)

WINDOWS = 'Windows'
LINUX = 'Linux'
MacOS = 'Darwin'
CURRENT_SYSTEM = platform.system()
logging.debug("CWD:{}, OS:{}, DEBUG:{}".format(os.getcwd(), CURRENT_SYSTEM, DEBUG))