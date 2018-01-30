# -*- coding: utf-8 -*-

from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
import pickle

from . import db
from .utils import utc2local


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    functions = db.relationship('Function', backref='author',
                                lazy='dynamic')
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow,
                          onupdate=datetime.utcnow)

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return "<User '{}'>".format(self.nickname)

    def hash_password(self, passwd):
        self.password_hash = pwd_context.encrypt(passwd)

    def verify_password(self, passwd):
        return pwd_context.verify(passwd, self.password_hash)


class Function(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    invoked = db.Column(db.Integer, index=True)
    code = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow,
                          onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(500))
    args = db.Column(db.String(500))
    lastin = db.Column(db.String(500))
    lastout = db.Column(db.String(500))
    # discrete data (array) of I:x and B/G:y
    data_x = db.Column(db.PickleType)
    data_y = db.Column(db.PickleType)
    # hit history with timestamp (array)
    hit_ts = db.Column(db.PickleType)

    hit_ts_list = []
    def append_hit_ts(self):
        """Append new ts to hit_ts.
        """
        self.hit_ts_list.append(self.timestamp)
        self.hit_ts = pickle.dumps(self.hit_ts_list)

    def get_hit_ts(self):
        try:
            return pickle.loads(self.hit_ts)
        except:
            return []

    def get_x(self):
        try:
            return pickle.loads(self.data_x)
        except:
            return []

    def get_y(self):
        try:
            return pickle.loads(self.data_y)
        except:
            return []

    def udef(self):
        return self.code.strip()

    def local_time(self):
        return utc2local(self.timestamp)

    def author_name(self):
        #return User.query.filter(User.id == 1).first().nickname
        return User.query.filter().first().nickname

    def __repr__(self):
        return "<Function '{}'>".format(self.name)

