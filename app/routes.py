# -*- coding: utf-8 -*-

from .models import Function
from .fields import function_fields
from flask_restful import marshal

from flask import Response
from flask import render_template
from flask import request

from app import app


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

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


@app.route('/help')
def help():
    return Response(
            render_template('help.html',
                title='Unicorn Service - Help',
                ),
            mimetype='text/html')


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return "Server shutting down..."
