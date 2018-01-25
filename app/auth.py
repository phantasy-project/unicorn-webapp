from flask_httpauth import HTTPBasicAuth
from flask import make_response
from flask import jsonify

from .models import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    u = User.query.filter(User.nickname==username).first()
    if not u:
        return False
    if u.verify_password(password):
        return True
    return False

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
