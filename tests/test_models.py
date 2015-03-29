# -*- coding: utf-8 -*-
"""
    fiddlersgreen.tests.test_models
    ~~~~~~~~~~~~~~~~~

    model tests

"""
import pytest

from fiddlersgreen.models import User, AnonymousUser


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
        assert name == '<User(\'longboxed\')>'
