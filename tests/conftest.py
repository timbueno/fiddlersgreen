# -*- coding: utf-8 -*-
"""
    fiddlersgreen.tests.conftest
    ~~~~~~~~~~~~~~~~~

    fiddlersgreen tests conftest setup module

"""
import pytest

from fiddlersgreen.frontend import create_app as create_frontend
from fiddlersgreen.core import db as _db
from fiddlersgreen.models import Role
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
def db(frontend_app):
    _db.app = frontend_app
    with frontend_app.app_context():
        _db.create_all()
        Role.insert_roles()

    yield _db

    _db.drop_all()
