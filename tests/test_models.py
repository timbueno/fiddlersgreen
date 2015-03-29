# -*- coding: utf-8 -*-
"""
    fiddlersgreen.tests.test_models
    ~~~~~~~~~~~~~~~~~

    model tests

"""
import pytest

from fiddlersgreen.models import User


@pytest.mark.usefixtures('db')
class TestUser:

    def test_get_by_id(self):
        user = User.create(
            social_id='twitter$timbueno',
            nickname='longboxed')
        user.save()

        retrieved = User.query.get(user.id)
        assert retrieved == user
        assert retrieved.social_id == 'twitter$timbueno'
    def test_repr(self):
        user = User.create(
            social_id='twitter$timbueno',
            nickname='longboxed')
        name = user.__repr__()
        assert name == '<User(\'longboxed\')>'
