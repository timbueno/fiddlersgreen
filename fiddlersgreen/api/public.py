# -*- coding: utf-8 -*-
"""
    fiddlersgreen.api.public
    ~~~~~~~~~~~~~~~~~

    Public api blueprint

"""
from flask import Blueprint
from flask.ext.login import login_required

from . import route


bp = Blueprint('public', __name__)


@route(bp, '/')
def index():
    return {'thing': '2'}


@route(bp, '/hidden')
@login_required
def hidden():
    return {'data': 'YOURE AUTHENTICATED'}
