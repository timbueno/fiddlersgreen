# -*- coding: utf-8 -*-
"""
    fiddlersgreen.users.models
    ~~~~~~~~~~~~~~~~~

    User models

"""
from datetime import datetime

from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from itsdangerous import JSONWebSignatureSerializer as Serializer

from ..core import bcrypt, db, Model, ReferenceCol


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
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=True)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    # Relationships
    role_id = ReferenceCol('roles', nullable=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User({email})>'.format(email=self.email)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_auth_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def ping(self):
        self.last_seen = datetime.utcnow()
        self.save()
