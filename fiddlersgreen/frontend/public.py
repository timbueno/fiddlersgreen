# -*- coding: utf-8 -*-
"""
    fiddlersgreen.frontend.public
    ~~~~~~~~~~~~~~~~~

    Public blueprints

"""
from flask import (Blueprint, current_app)
from flask.ext.login import login_required

from . import route


bp = Blueprint('public', __name__)


@route(bp, '/')
def index():
    return current_app.config.get('SQLALCHEMY_DATABASE_URI')


@route(bp, '/hidden')
@login_required
def hidden():
    return 'You\'re authenticated!'
