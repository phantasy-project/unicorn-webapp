import os

DEBUG = False
#SERVER_NAME = '192.168.31.115:5000'

basedir = os.path.abspath(os.path.dirname(__file__))

# SQLite
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# MySQL
SQLALCHEMY_DATABASE_URI = \
    'mysql+pymysql://{username}:{password}@{host}/unicorn'.format(
        username='dev',
        password='dev',
        host='localhost')

SQLALCHEMY_TRACK_MODIFICATIONS = False
