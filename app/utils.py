# -*- coding: utf-8 -*-

from datetime import datetime
import pytz
import tzlocal


def utc2local(u_time):
    l_tz = tzlocal.get_localzone()
    l_time = u_time.replace(tzinfo=pytz.utc).astimezone(l_tz)
    return l_time.strftime("%Y-%m-%d %H:%M:%S %Z")

