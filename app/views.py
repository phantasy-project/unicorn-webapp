# -*- coding: utf-8 -*-

from flask import jsonify
from flask import abort
from flask import request
from flask import make_response
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields
from flask_restful import marshal

from .models import functions
from .auth import auth

try:
    unicode
except:
    unicode = str

function_fields = {
    'name': fields.String,
    'description': fields.String,
    'invoked': fields.Integer,
    'uri': fields.Url('function', absolute=True)
}


class FunctionAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.rp = reqparse.RequestParser()
        self.rp.add_argument('name', type=str, location='json')
        self.rp.add_argument('description', type=str, location='json')
        self.rp.add_argument('invoked', type=int, location='json')
        super(FunctionAPI, self).__init__()

    def get(self, name):
        func = [f for f in functions if f['name'] == name]
        if func == []:
            abort(404)
        return {'function': marshal(func[0], function_fields)}

    def put(self, name):
        func = [f for f in functions if f['name'] == name]
        if func == []:
            abort(404)
        f = func[0]
        args = self.rp.parse_args()
        for k, v in args.items():
            if v is not None:
                f[k] = v
        return {'function': marshal(f, function_fields)}

    def delete(self, name):
        func = [f for f in functions if f['name'] == name]
        if func == []:
            abort(404)
        functions.remove(func[0])
        return {'result': True}


class FunctionListAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.rp = reqparse.RequestParser()
        self.rp.add_argument('name', type=str, required=True,
                help='No function name provided', location='json')
        self.rp.add_argument('description', type=str, default='',
                location='json')
        super(FunctionListAPI, self).__init__()

    def get(self):
        return {'functions': [marshal(f, function_fields) for f in functions]}

    def post(self):
        func = self.rp.parse_args()
        if func.get('name') in [i['name'] for i in functions]:
            return {'error': 'function exists'}, 400
        else:
            functions.append(func)
            return {'function': marshal(func, function_fields)}, 201


#def gen_uri(func):
#    new_func = {}
#    for k in func:
#        if k == 'name':
#            new_func['uri'] = api.url_for(FunctionAPI, name=func['name'],
#                    _external=True)
#        else:
#            new_func[k] = func[k]
#    return new_func

