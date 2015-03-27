# -*- coding: utf-8 -*-
"""
    fiddlersgreen.tests.test_config
    ~~~~~~~~~~~~~~~~~

    configuration tests

"""
from fiddlersgreen.frontend import create_app
from fiddlersgreen.settings import config, DevConfig


def test_config_dict():
    for env in ['dev', 'test', 'default']:
        assert config[env]


def test_dev_config():
    c = config['dev']
    assert c == DevConfig
    app = create_app(c)
    assert app.config['DB_NAME'] == 'dev.db'
    assert app.config['DEBUG'] is True
