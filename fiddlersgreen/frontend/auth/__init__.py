# -*- coding: utf-8 -*-
"""
    fiddlersgreen.frontend.auth
    ~~~~~~~~~~~~~~~~~

    Frontend Authentication Module

"""
from flask import Blueprint

bp = Blueprint('auth', __name__)

from . import views  # NOQA
