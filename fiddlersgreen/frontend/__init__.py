# -*- coding: utf-8 -*-
"""
    fiddlersgreen.frontend
    ~~~~~~~~~~~~~~~~~

    launchpad frontend application package

"""
from functools import wraps

from .. import factory


def create_app(config):
    """Returns the frontend application instance"""
    app = factory.create_app(__name__, __path__, config)

    return app


def route(bp, *args, **kwargs):
    """Route decorator for use in blueprints"""
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator
