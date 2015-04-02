# -*- coding: utf-8 -*-
"""
    fiddlersgreen.api
    ~~~~~~~~~~~~~~~~~

    launchpad api application package

"""
from functools import wraps

from flask import jsonify

from .errors import (bad_request, unauthorized, forbidden, not_found,
                     internal_server_error)
from .. import factory
from ..helpers import JSONEncoder


def create_app(config):
    """Returns the api application instance"""
    app = factory.create_app(__name__, __path__, config)

    # Set the default JSON encoder
    app.json_encoder = JSONEncoder

    # Register api app specific extensions
    register_extensions(app)

    # Register error handlers
    register_errorhandlers(app)

    return app


def register_extensions(app):
    return None


def register_errorhandlers(app):
    app.errorhandler(400)(bad_request)
    app.errorhandler(401)(unauthorized)
    app.errorhandler(403)(forbidden)
    app.errorhandler(404)(not_found)
    app.errorhandler(500)(internal_server_error)


def route(bp, *args, **kwargs):
    """Route decorator for use in blueprints"""
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            sc = 200
            rv = f(*args, **kwargs)
            if isinstance(rv, tuple):
                sc = rv[1]
                rv = rv[0]
            return jsonify(dict(data=rv)), sc
        return f

    return decorator
