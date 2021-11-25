import sys
import pytz
import datetime as dt
import pandas as pd


def convert_date_to_utc(time_zone, dt_str, t_format="%Y-%m-%d"):
    if(dt_str == ''):
        return None
    if isinstance(dt_str, dt.date):
        dt_str = dt_str.strftime(t_format)
    naive = dt.datetime.strptime(dt_str, t_format)
    local = pytz.timezone(time_zone)
    local_date = local.localize(naive, is_dst=True)
    return local_date.astimezone(pytz.utc).replace(tzinfo=None)


def convert_date_to_utc_with_hours(time_zone, dt_str, t_format="%Y-%m-%d %H:%M:%S"):
    if(dt_str == ''):
        return None
    if isinstance(dt_str, dt.date):
        dt_str = dt_str.strftime(t_format)
    naive = dt.datetime.strptime(dt_str, t_format)
    local = pytz.timezone(time_zone)
    local_date = local.localize(naive, is_dst=True)
    return local_date.astimezone(pytz.utc).replace(tzinfo=None)
