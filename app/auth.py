from flask_httpauth import HTTPBasicAuth
from flask import make_response
from flask import jsonify


auth = HTTPBasicAuth()

users = {
    'dev': 'dev',
}

@auth.get_password
def get_password(username):
    if username in users:
        return users.get(username)
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
