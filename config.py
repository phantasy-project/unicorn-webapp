import os

DEBUG = False

basedir = os.path.abspath(os.path.dirname(__file__))

# SQLite
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# MySQL
SQLALCHEMY_DATABASE_URI = \
    'mysql+pymysql://{username}:{password}@{host}/unicorn'.format(
        username='unicorn',
        password='unicorn#',
        host='localhost')

SQLALCHEMY_TRACK_MODIFICATIONS = False
