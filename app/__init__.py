# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

api = Api(app)


from .views import FunctionAPI, FunctionListAPI

api.add_resource(FunctionAPI, '/api/v2.0/functions/<string:name>',
                 endpoint='function')
api.add_resource(FunctionListAPI, '/api/v2.0/functions',
                 endpoint='functions')
