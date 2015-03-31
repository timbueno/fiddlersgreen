#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~~~~~~~~~~~~

    manage module

"""
import os

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Shell, Server

from fiddlersgreen import frontend
from fiddlersgreen.core import db
from fiddlersgreen.models import User
from fiddlersgreen.settings import config as app_config


config = app_config[os.environ.get('APP_ENV') or 'default']
app = frontend.create_app(config)

manager = Manager(app)
migrate = Migrate(app, db)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default
    """
    return {'app': app, 'User': User}


# Add commands to the manager
manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
