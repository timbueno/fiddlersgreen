# -*- coding: utf-8 -*-
"""
    fiddlersgreen.users.models
    ~~~~~~~~~~~~~~~~~

    User models

"""
from flask.ext.login import UserMixin, AnonymousUserMixin
from ..core import db, Model


class AnonymousUser(AnonymousUserMixin):
    pass


class User(Model, UserMixin):
    __tablename__ = 'users'
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return '<User({nickname})>'.format(nickname=self.nickname)
