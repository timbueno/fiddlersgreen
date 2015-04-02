# -*- coding: utf-8 -*-
"""
    fiddlersgreen.frontend
    ~~~~~~~~~~~~~~~~~

    launchpad frontend application package

"""
from functools import wraps

from .. import factory
from ..core import bootstrap


def create_app(config):
    """Returns the frontend application instance"""
    app = factory.create_app(__name__, __path__, config)

    register_extensions(app)

    return app


def register_extensions(app):
    bootstrap.init_app(app)
    return None


def route(bp, *args, **kwargs):
    """Route decorator for use in blueprints"""
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator
