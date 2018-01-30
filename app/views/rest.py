# -*- coding: utf-8 -*-

from datetime import datetime

from flask import abort
from flask import request
from flask import render_template
from flask import Response
from flask import make_response

from flask_restful import Resource
from flask_restful import marshal
from flask_restful import reqparse

from ..models import Function, User
from ..models import db
from ..auth import auth
from ..utils import check_code
from ..utils import eval_code
from ..fields import function_fields
from ..viz import create_data_plot
from ..viz import create_trend_plot


def request_json():
    best = request.accept_mimetypes \
            .best_match(['application/json', 'text/html'])
    return best == 'application/json'


class FunctionAPI(Resource):
    #decorators = [auth.login_required]
    def __init__(self):
        self.rp = reqparse.RequestParser()
        self.rp.add_argument('name', type=str, location='json')
        self.rp.add_argument('args', type=str, location='json')
        self.rp.add_argument('description', type=str, location='json')
        self.rp.add_argument('code', type=str, location='json')
        self.rp.add_argument('data_x', type=str, location='json')
        self.rp.add_argument('data_y', type=str, location='json')
        super(FunctionAPI, self).__init__()

    def get(self, name):
        func = Function.query.filter(Function.name==name).first()
        if func is None:
            abort(404)
        data_script, data_div = create_data_plot(func)
        trend_script, trend_div = create_trend_plot(func)

        f = marshal(func, function_fields)

        if request_json():
            return {'function': funcs}
        return Response(
                    render_template('show_item.html',
                        title="Unicorn - Function",
                        item=f,
                        data_div=data_div, data_script=data_script,
                        trend_div=trend_div, trend_script=trend_script,
                        ),
                    mimetype='text/html')

    @auth.login_required
    def put(self, name):
        func = Function.query.filter(Function.name==name).first()
        if func is None:
            abort(404)
        args = self.rp.parse_args()
        for k, v in args.items():
            if v is not None:
                if k in ['code']:
                    v = check_code(v)
                setattr(func, k, v)

        db.session.commit()
        return {'function': marshal(func, function_fields)}

    @auth.login_required
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
        self.rp.add_argument('code', type=str, required=True,
                help='No code found', location='json')
        self.rp.add_argument('description', type=str, default='TBA',
                location='json')
        self.rp.add_argument('args', type=str, default='',
                location='json')
        self.rp.add_argument('author', type=str, default='',
                location='json')
        self.rp.add_argument('data_x', type=str, default='',
                location='json')
        self.rp.add_argument('data_y', type=str, default='',
                location='json')
        super(FunctionListAPI, self).__init__()

    def get(self):
        fs = Function.query.all()
        if request_json():
            return {'functions': [marshal(f, function_fields) for f in fs]}
        return Response(
                    render_template('show_items.html',
                        title="Unicorn - Functions",
                        items=[marshal(f, function_fields) for f in fs]),
                        mimetype='text/html')

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
                    u = User.query.all()[0]
                else: # does not work
                    u = User(nickname=func.get('author'), email='TBA')
                    db.session.add(u)

            code = check_code(func.get('code'))
            if not code:
                return {"error": "Invalid code"}, 406

            new_f = Function(name=f_name, invoked=0,
                             timestamp=datetime.utcnow(),
                             author=u,
                             code=code,
                             description=func.get('description'),
                             args=func.get('args'),
                             data_x=func.get('data_x'),
                             data_y=func.get('data_y'),
                    )
            db.session.add(new_f)
            db.session.commit()
            return {'function': marshal(new_f, function_fields)}, 201


class FunctionExecAPI(Resource):
    def get(self, name):
        func = Function.query.filter(Function.name==name).first()
        if func is None:
            abort(404)
        inp, oup = eval_code(func, **dict(request.args.items()))
        if inp is not None and oup is not None:
            setattr(func, 'lastin', str(inp))
            setattr(func, 'lastout', str(oup))
            setattr(func, 'invoked', func.invoked + 1)
            func.append_hit_ts()
            db.session.commit()

        #else:
        #    setattr(func, 'invoked', func.invoked + 1)
        #    db.session.commit()

        return {'result': oup}
