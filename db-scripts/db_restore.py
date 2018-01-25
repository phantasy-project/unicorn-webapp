#!/usr/bin/env python
# -*- coding: utf8 -*-

"""Initialize db.
"""

from datetime import datetime

import sys
sys.path.insert(0, '../')


from app.models import Function
from app.models import db


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

db.session.commit()
