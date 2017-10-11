# -*- coding: utf-8 -*-

from datetime import datetime

from flask import abort
from flask import request
from flask import render_template
from flask import Response

from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal
from flask_restful import reqparse

from ..models import Function, User
from ..models import db
from ..auth import auth


function_fields = {
    'name': fields.String,
    'definition': fields.String,
    'invoked': fields.Integer,
    'author': fields.String(attribute=lambda x: x.author_name()),
    'uri': fields.Url('function', absolute=True),
    'timestamp': fields.String(attribute=lambda x:x.local_time()),
    'desc': fields.String(),
    'args': fields.String(),
    'lastout': fields.String(),
}

def request_json():
    best = request.accept_mimetypes \
            .best_match(['application/json', 'text/html'])
    return best == 'application/json'


class FunctionAPI(Resource):
    #decorators = [auth.login_required]
    def __init__(self):
        self.rp = reqparse.RequestParser()
        self.rp.add_argument('name', type=str, location='json')
        self.rp.add_argument('desc', type=str, location='json')
        self.rp.add_argument('definition', type=str, location='json')
        super(FunctionAPI, self).__init__()

    def get(self, name):
        func = Function.query.filter(Function.name==name).first()
        if func is None:
            abort(404)

        inp, oup = eval_func(func, **dict(request.args.items()))
        if inp is not None and oup is not None:
            setattr(func, 'args', inp)
            setattr(func, 'lastout', oup)
            db.session.commit()
        
        if request_json():
            return {'function': marshal(func, function_fields)}
        return Response(
                    render_template('show_entries.html',
                        function=marshal(func, function_fields)), 
                    mimetype='text/html')

    @auth.login_required
    def put(self, name):
        # todo: handle user?
        func = Function.query.filter(Function.name==name).first()
        if func is None:
            abort(404)
        args = self.rp.parse_args()
        for k, v in args.items():
            if v is not None:
                setattr(func, k, v)
        db.session.commit()
        return {'function': marshal(func, function_fields)}

    def delete(self, name):
        func = Function.query.filter(Function.name==name).first()
        if func is None:
            abort(404)
        db.session.delete(func)
        db.session.commit()
        return {'result': True}


class FunctionListAPI(Resource):
    #decorators = [auth.login_required]
    def __init__(self):
        self.rp = reqparse.RequestParser()
        self.rp.add_argument('name', type=str, required=True,
                help='No function name provided', location='json')
        self.rp.add_argument('definition', type=str, required=True,
                help='No definition found', location='json')
        self.rp.add_argument('desc', type=str, default='',
                location='json')
        self.rp.add_argument('args', type=str, default='x',
                location='json')
        self.rp.add_argument('author', type=str, default='',
                location='json')
        super(FunctionListAPI, self).__init__()

    def get(self):
        fs = Function.query.all()
        return {'functions': [marshal(f, function_fields) for f in fs]}

    @auth.login_required
    def post(self):
        func = self.rp.parse_args()
        f_name = func.get('name')
        f = Function.query.filter(Function.name==f_name).first()
        if f is not None:
            return {'error': 'function exists'}, 400
        else:
            u = User.query.filter(User.nickname==func.get('author')).first()
            if u is None:
                if func.get('author') == '':
                    u = User.query.get(1)
                else: # does not work
                    u = User(nickname=func.get('author'), email='TBA')
                    db.session.add(u)
                print(u)

            new_f = Function(name=f_name, invoked=0,
                             timestamp=datetime.utcnow(),
                             author=u,
                             definition=func.get('definition'),
                             desc=func.get('desc', 'TBA'),
                             args=func.get('args'),
                    )
            db.session.add(new_f)
            db.session.commit()
            return {'function': marshal(new_f, function_fields)}, 201


def eval_func(f, **kws):
    fncode, ns = compile(f.definition, "<string>", "exec"), {}
    exec fncode in ns
    try:
        x = float(kws.values()[0])
    except IndexError:
        return None, None
    return x, ns.get('f')(x)



    
