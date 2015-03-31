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

    def test_get_by_id(self):
        user = User.create(email='timbueno@gmail.com')
        retrieved = User.query.get(user.id)
        assert retrieved == user

    def test_is_not_anonymous(self):
        user = User.create(email='timbueno@gmail.com')
        assert user.is_anonymous() is False

    def test_is_anonymous(self):
        user = AnonymousUser()
        assert user.is_anonymous()

    def test_repr(self):
        user = User.create(email='timbueno@gmail.com')
        name = user.__repr__()
        assert name == '<User(timbueno@gmail.com)>'

    def test_default_role(self):
        user = User.create(email='timbueno@gmail.com')
        assert user.role.default

    def test_password_setter(self):
        user = User.create(email='timbueno@gmail.com', password='cat')
        assert user.password_hash is not None

    def test_no_password_getter(self):
        user = User.create(email='timbueno@gmail.com', password='cat')
        with pytest.raises(AttributeError):
            user.password

    def test_password_verification(self):
        user = User.create(email='timbueno@gmail.com', password='cat')
        assert user.verify_password('cat')

    def test_password_salts_are_random(self):
        u1 = User.create(email='timbueno@gmail.com', password='cat')
        u2 = User.create(email='longboxed@gmail.com', password='cat')
        assert u1.password_hash != u2.password_hash

    def test_ping(self):
        user = User.create(email='timbueno@gmail.com', password='cat')
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
