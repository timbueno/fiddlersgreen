# -*- coding: utf-8 -*-
"""
    fiddlersgreen.api.auth
    ~~~~~~~~~~~~~~~~~

    Authentication api blueprint

"""
from flask import Blueprint
from flask.ext.login import current_user, login_required

from . import route
from ..core import login_manager
from ..models import User


bp = Blueprint('auth', __name__)


@login_manager.request_loader
def load_user_from_request(request):
    # First try to load user from api key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = User.verify_auth_token(api_key)
        if user:
            return user
    # Finally, return None if no user was logged in
    return None


@route(bp, '/token')
@login_required
def get_token():
    print(current_user.get_auth_token())
    return dict(token=current_user.get_auth_token())
