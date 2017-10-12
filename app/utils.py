# -*- coding: utf-8 -*-

from datetime import datetime
import pytz
import tzlocal

from yapf.yapflib.yapf_api import FormatCode


def utc2local(u_time):
    l_tz = tzlocal.get_localzone()
    l_time = u_time.replace(tzinfo=pytz.utc).astimezone(l_tz)
    return l_time.strftime("%Y-%m-%d %H:%M:%S %Z")


def check_code(code):
    try:
        ret,_ = FormatCode(code.strip())
    except:
        ret = False
    return ret


def to_dict(d):
    ret = {}
    for k,v in d.items():
        try:
            ret[k] = float(v)
        except:
            ret[k] = v
    return ret


def eval_code(f, **kws):
    kwargs = to_dict(kws)
    print(kwargs)
    fncode, ns = compile(f.code, "<string>", "exec"), {}
    exec fncode in ns
    if not f.args:
        return kwargs, ns.get('f')(**kwargs)
    else:
        kvs = {k:v for k,v in kwargs.items() if k in f.args.split(',')}
        return kvs, ns.get('f')(**kvs)
