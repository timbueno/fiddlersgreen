#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~~~~~~~~~~~~

    manage module

"""
import os

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Shell
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from fiddlersgreen import frontend, api
from fiddlersgreen.core import db
from fiddlersgreen.models import User
from fiddlersgreen.settings import config as app_config


config = app_config[os.environ.get('APP_ENV') or 'default']
frontend_app = frontend.create_app(config)
api_app = api.create_app(config)

application = DispatcherMiddleware(frontend_app, {
    '/api/v1': api_app
})

manager = Manager(api_app)
migrate = Migrate(api_app, db)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default
    """
    return {'app': api_app, 'User': User}

# Create the server
# server = Server(application=application, port=5000)


# Add commands to the manager
@manager.command
def server():
    run_simple('0.0.0.0', 5000, application, use_reloader=True,
               use_debugger=True)
    return None
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
