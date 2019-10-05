import os
from .apps import AttendanceConfig

default_app_config = 'attendance.AttendanceConfig'


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]
