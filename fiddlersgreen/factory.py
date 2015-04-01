# -*- coding: utf-8 -*-
"""
    fiddlersgreen.factory
    ~~~~~~~~~~~~~~~~~

    fiddlersgreen factory module

"""
import pkgutil
import importlib

from flask import (Blueprint, Flask)

from .core import bcrypt, db, login_manager


def create_app(package_name, package_path, config):
    # Create the app
    app = Flask(package_name, instance_relative_config=True)

    # Configure the app
    app.config.from_object(config)
    app.config.from_pyfile('settings.cfg', silent=True)

    register_extensions(app)
    register_errorhandlers(app)
    register_blueprints(app, package_name, package_path)

    return app


def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    return None


def register_errorhandlers(app):
    return None


def register_blueprints(app, package_name, package_path):
    """Register all Blueprint instances on the specified Flask application
    found in all modules for the specified package."""
    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('{:s}.{:s}'.format(package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv
