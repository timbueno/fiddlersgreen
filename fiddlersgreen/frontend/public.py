# -*- coding: utf-8 -*-
"""
    fiddlersgreen.frontend.public
    ~~~~~~~~~~~~~~~~~

    Public blueprints

"""
from flask import (Blueprint, current_app)

from . import route


bp = Blueprint('public', __name__)


@route(bp, '/')
def index():
    return current_app.config.get('SQLALCHEMY_DATABASE_URI')
