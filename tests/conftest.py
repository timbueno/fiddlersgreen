# -*- coding: utf-8 -*-
"""
    fiddlersgreen.tests.conftest
    ~~~~~~~~~~~~~~~~~

    fiddlersgreen tests conftest setup module

"""
import pytest

from fiddlersgreen.frontend import create_app as f_create_app
from fiddlersgreen.settings import config as app_config


@pytest.yield_fixture(scope='function')
def frontend_app():
    config = app_config['test']
    _app = f_create_app(config)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()
