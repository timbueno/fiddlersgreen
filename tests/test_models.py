# -*- coding: utf-8 -*-
"""
    fiddlersgreen.tests.test_models
    ~~~~~~~~~~~~~~~~~

    model tests

"""
import pytest

from fiddlersgreen.models import User, AnonymousUser, Role


@pytest.mark.usefixtures('db')
class TestUser:

    def test_get_by_id(self):
        user = User.create(
            social_id='twitter$timbueno',
            nickname='longboxed')

        retrieved = User.query.get(user.id)
        assert retrieved == user
        assert retrieved.social_id == 'twitter$timbueno'

    def test_is_not_anonymous(self):
        user = User.create(
            social_id='twitter$timbueno',
            nickname='longboxed')
        assert user.is_anonymous() is False

    def test_is_anonymous(self):
        user = AnonymousUser()
        assert user.is_anonymous()

    def test_repr(self):
        user = User.create(
            social_id='twitter$timbueno',
            nickname='longboxed')
        name = user.__repr__()
        assert name == '<User(longboxed)>'


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
