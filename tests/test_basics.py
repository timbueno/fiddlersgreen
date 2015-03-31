# -*- coding: utf-8 -*-
"""
    fiddlersgreen.tests.test_basics
    ~~~~~~~~~~~~~~~~~

    fiddlersgreen basic tests module

"""
from flask import current_app


def test_app_exists(frontend_app):
    assert current_app is not None


def test_app_is_testing(frontend_app):
    assert frontend_app.config.get('TESTING')
