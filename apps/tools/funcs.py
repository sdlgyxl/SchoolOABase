# -*- coding: utf-8 -*-
"""
@File    : funcs.py
@Time    : 2019-09-01 20:09
@Author  : 杨小林
"""
from datetime import datetime, timedelta

def get_prev_month(d):
    """
    返回上个月第一个天和最后一天的日期时间
    :return
    date_from: 2016-01-01 00:00:00
    date_to: 2016-01-31 23:59:59
    """
    dayscount = timedelta(days=d.day)
    dayto = d - dayscount
    date_from = datetime(dayto.year, dayto.month, 1, 0, 0, 0)
    date_to = datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
    return date_from, date_to
