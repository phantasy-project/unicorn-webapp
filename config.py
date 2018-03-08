# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser


def find_conf():
    """Find additional configuration file for unicorn service,
    searching the following locations:
    * ~/.unicorn/unicorn.ini
    * /etc/unicorn/unicorn.ini
    * pacakge root location
    """
    home_conf = os.path.expanduser('~/.unicorn/unicorn.ini')
    sys_conf = '/etc/unicorn/unicorn.ini'
    if os.path.isfile(home_conf):
        return home_conf
    elif os.path.isfile(sys_conf):
        return sys_conf
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(basedir, 'unicorn.ini')


conf = ConfigParser()
conf.read(find_conf())
db_user, db_pass = conf['DATABASE']['username'], conf['DATABASE']['password']
db_host, db_name = conf['DATABASE']['hostname'], conf['DATABASE']['database']

# MySQL/MariaDB
SQLALCHEMY_DATABASE_URI = \
    'mysql+pymysql://{username}:{password}@{hostname}/{database}'.format(
        username=db_user,
        password=db_pass,
        hostname=db_host,
        database=db_name)

SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = conf['LOGGING']['debug'].lower() == 'true'
