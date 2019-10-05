import os
from django.apps import AppConfig
from .apps import BaseConfig

default_app_config = 'base.BaseConfig'


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]
