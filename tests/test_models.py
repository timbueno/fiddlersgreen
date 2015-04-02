# -*- coding: utf-8 -*-
"""
    fiddlersgreen.tests.test_models
    ~~~~~~~~~~~~~~~~~

    model tests

"""
import time

import pytest

from fiddlersgreen.models import User, AnonymousUser, Role


@pytest.mark.usefixtures('db')
class TestUser:

    def test_get_by_id(self, user):
        retrieved = User.query.get(user.id)
        assert retrieved == user

    def test_is_not_anonymous(self, user):
        assert user.is_anonymous() is False

    def test_is_anonymous(self):
        user = AnonymousUser()
        assert user.is_anonymous()

    def test_repr(self, user):
        name = user.__repr__()
        assert name == '<User(timbueno@gmail.com)>'

    def test_default_role(self, user):
        assert user.role.default

    def test_password_setter(self, user):
        assert user.password_hash is not None

    def test_no_password_getter(self, user):
        with pytest.raises(AttributeError):
            user.password

    def test_password_verification(self, user):
        assert user.verify_password('cat')

    def test_password_salts_are_random(self):
        u1 = User.create(email='timbueno@gmail.com', password='cat')
        u2 = User.create(email='longboxed@gmail.com', password='cat')
        assert u1.password_hash != u2.password_hash

    def test_get_auth_token(self, user):
        token = user.get_auth_token()
        assert token

    def test_verify_auth_token(self, user):
        token = user.get_auth_token()
        retrieved = User.verify_auth_token(token)
        assert retrieved == user

    def test_verify_auth_token_password_change(self, user):
        token = user.get_auth_token()
        # Token should not change
        assert token == user.get_auth_token()
        # Change password
        user.password = 'dog'
        user.save()
        # Token should be different
        new_token = user.get_auth_token()
        assert token != new_token

    def test_ping(self, user):
        last_seen_before = user.last_seen
        time.sleep(1)
        user.ping()
        assert user.last_seen > last_seen_before


@pytest.mark.usefixtures('db')
class TestRole:

    def test_insert_roles(self):
        from fiddlersgreen.models import ROLES
        Role.insert_roles()
        for r in ROLES.keys():
            role = Role.query.filter_by(name=r).first()
            assert role
            assert role.name == r
            assert role.default is ROLES[r][0]
