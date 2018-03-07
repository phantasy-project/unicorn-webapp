#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Initialize admin user
"""

import sys
sys.path.insert(0, '/usr/share/unicorn')

from app.models import User
from app.models import db

_admin0 = {'name': 'uadmin', 'hash': '$6$rounds=656000$BGPNku.GTxUFp5/m$z2VoGUbOzZfjEq2TnQjyK4Ho47MYCEHEK5N/TjpgzNuLWOJHwoeIA3AUbbDSMEvQBdqtEv1Vez1OXAYtYc4r80'}

user0 = User(nickname=_admin0['name'], password_hash=_admin0['hash'], 
             email='admin@localhost', id=1)

# default admin account
db.session.add(user0)
db.session.commit()
