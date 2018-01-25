# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '../templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '../static')

app = Flask(__name__,
            template_folder=template_dir,
            static_folder=static_dir)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)


from .models import Function
from .fields import function_fields
from flask_restful import marshal

from flask import Response
from flask import render_template

@app.route('/')
def index():
    fs = Function.query.all()
    #funcs = sorted([marshal(f, function_fields) for f in fs],
    #        key=lambda x:x['invoked'], reverse=True)[:100]
    funcs = [marshal(f, function_fields) for f in fs] # sort by dataTables.
    return Response(
            render_template('index.html',
                title='Unicorn Service',
                funcs=funcs),
            mimetype='text/html')


from .views import FunctionAPI
from .views import FunctionListAPI
from .views import FunctionExecAPI


api.add_resource(FunctionAPI, '/functions/<string:name>',
                 endpoint='function')
api.add_resource(FunctionListAPI, '/functions',
                 endpoint='functions')
api.add_resource(FunctionExecAPI, '/api/v1.0/functions/<string:name>',
                 endpoint='func')
