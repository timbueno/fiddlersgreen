# -*- coding: utf-8 -*-
"""
    fiddlersgreen.users.models
    ~~~~~~~~~~~~~~~~~

    User models

"""
from flask.ext.login import UserMixin, AnonymousUserMixin
from ..core import db, Model, ReferenceCol


ROLES = {
    'User': (True,),
    'Moderator': (False,),
    'Administrator': (False,)
}


class Role(Model):
    __tablename__ = 'roles'
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)

    @staticmethod
    def insert_roles():
        for r in ROLES.keys():
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role.new(name=r)
            role.default = ROLES[r][0]
            db.session.add(role)
        db.session.commit()


class AnonymousUser(AnonymousUserMixin):
    pass


class User(Model, UserMixin):
    __tablename__ = 'users'
    role_id = ReferenceCol('roles', nullable=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User({nickname})>'.format(nickname=self.nickname)
