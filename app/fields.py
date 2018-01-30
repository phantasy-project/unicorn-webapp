# -*- coding: utf-8 -*-

from flask_restful import fields


function_fields = {
    'name': fields.String,
    'udef': fields.String(attribute=lambda x:x.udef()),
    'code': fields.String,
    'invoked': fields.Integer,
    'author': fields.String(attribute=lambda x: x.author_name()),
    'uri': fields.Url('function', absolute=True),
    'uri-api': fields.Url('func', absolute=True),
    'timestamp': fields.String(attribute=lambda x:x.local_time()),
    'description': fields.String,
    'args': fields.String,
    'lastin': fields.String,
    'lastout': fields.String,
    #'x': fields.Raw(attribute=lambda x:x.get_x()),
    #'y': fields.Raw(attribute=lambda x:x.get_y()),
}
