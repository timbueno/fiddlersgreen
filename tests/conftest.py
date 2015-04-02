# -*- coding: utf-8 -*-
"""
    fiddlersgreen.tests.conftest
    ~~~~~~~~~~~~~~~~~

    fiddlersgreen tests conftest setup module

"""
import pytest

from fiddlersgreen.api import create_app as create_api
from fiddlersgreen.frontend import create_app as create_frontend
from fiddlersgreen.core import db as _db
from fiddlersgreen.models import Role, User
from fiddlersgreen.settings import config as app_config


@pytest.yield_fixture(scope='function')
def frontend_app():
    config = app_config['test']
    _app = create_frontend(config)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def api_app():
    config = app_config['test']
    _app = create_api(config)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def db(api_app):
    _db.app = api_app
    with api_app.app_context():
        _db.create_all()
        Role.insert_roles()

    yield _db

    _db.drop_all()


@pytest.fixture
def user(db):
    return User.create(email='timbueno@gmail.com', password='cat')
