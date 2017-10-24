import os

DEBUG = False
#SERVER_NAME = '192.168.31.115:5000'

basedir = os.path.abspath(os.path.dirname(__file__))

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = \
    'mysql+pymysql://{username}:{password}@{host}/unicorn'.format(
        username='dev',
        password='dev',
        host='localhost')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
