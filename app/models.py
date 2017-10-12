# -*- coding: utf-8 -*-

from datetime import datetime

from . import db
from .utils import utc2local


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    functions = db.relationship('Function', backref='author',
                                lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
    
    def __repr__(self):
        return "<User '{}'>".format(self.nickname)


class Function(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    invoked = db.Column(db.Integer, index=True)
    code = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,
                          default=datetime.utcnow,
                          onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(100))
    args = db.Column(db.String(20))
    lastin = db.Column(db.String(20))
    lastout = db.Column(db.String(20))

    def local_time(self):
        return utc2local(self.timestamp)

    def author_name(self):
        return User.query.filter(User.id == 1).first().nickname
    
    def __repr__(self):
        return "<Function '{}'>".format(self.name)
