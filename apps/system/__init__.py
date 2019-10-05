import os
from django.apps import AppConfig
from .apps import SystemConfig

default_app_config = 'system.SystemConfig'


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]
