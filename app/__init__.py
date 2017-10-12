# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')

app = Flask(__name__,
            instance_relative_config=True,
            template_folder=template_dir,
            static_folder=static_dir)
app.config.from_object('config')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)


from .views import FunctionAPI
from .views import FunctionListAPI
from .views import FunctionExecAPI

api.add_resource(FunctionAPI, '/functions/<string:name>',
                 endpoint='function')
api.add_resource(FunctionListAPI, '/functions',
                 endpoint='functions')
api.add_resource(FunctionExecAPI, '/api/functions/<string:name>',
                 endpoint='func')
