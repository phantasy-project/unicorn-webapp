#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Initialize admin account for unicorn app.
"""

import sys
sys.path.insert(0, '/usr/share/unicorn')

from passlib.apps import custom_app_context as pwd_context
import getpass

admin_name = getpass.getuser() 
print("Current user name is: {}.".format(admin_name))
admin_email = input("Set the email: ")
admin_pass_verify = True
admin_pass = False
while admin_pass_verify != admin_pass:
    admin_pass = getpass.getpass(prompt="Set password: ")
    admin_pass_verify = getpass.getpass(prompt="Verify password: ")

admin_account = {'name': admin_name,
                 'hash': pwd_context.encrypt(admin_pass),
                 'email': admin_email}

from app.models import User
from app.models import db

u0 = User(nickname=admin_account['name'],
          password_hash=admin_account['hash'], 
          email=admin_account['email'], id=1)

u = User.query.filter(User.nickname==admin_name).first()
if u is None:
    db.session.add(u0)
    print("Create new admin user: {}".format(admin_name))
else:
    print("Update admin user: {}".format(admin_name))
    for k,v in admin_account.items():
        setattr(u, k, v)

db.session.commit()
