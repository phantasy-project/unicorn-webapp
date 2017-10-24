#!/usr/bin/env python
# -*- coding: utf8 -*-

"""Initialize db.
"""

from datetime import datetime

import sys
sys.path.insert(0, '../')

from app.models import Function
from app.models import User
from app.models import db


u1 = User(nickname='dev1', email='dev1@localhost', id=1)


# read json data into db
import json
from datetime import datetime
import os

infile = os.path.join(os.path.dirname(__file__), 'app.json')
data = json.load(open(infile, 'r'))

for rec in data:
    kws = {}
    for k,v in rec.items():
        if k == 'timestamp':
            kws[k] = datetime.strptime(v,'%Y-%m-%d %H:%M:%S.%f')
        elif k != 'id':
            kws[k] = v
    f = Function(**kws)
    db.session.add(f)

# users:
db.session.add(u1)
db.session.commit()

#f2_str = """
#def f(x):
#    return 1 + 0.5*x + 0.25*x**2.0
#"""
#
#f2 = Function(name='f2', invoked=0,
#              timestamp=datetime.utcnow(),
#              author=u1,
#              args='x',
#              code=f2_str,
#              description="complex math equation")
