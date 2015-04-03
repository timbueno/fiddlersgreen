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
    # api_key = request.headers.get('Authorization')
    auth = request.authorization
    if auth:
        email_or_token = auth.username
        password = auth.password
    else:
        email_or_token = ''
        password = ''
    # Check for email or token, abort if not provided
    if email_or_token == '':
        return None
    # If email_or_token is set but password is not, run the token auth
    if password == '':
        user = User.verify_auth_token(email_or_token)
        return user

    # Try basic authentication
    user = User.query.filter_by(email=email_or_token).first()
    if user:
        if user.verify_password(password):
            return user

    # Finally, return None if no user was logged in
    return None


@route(bp, '/token')
@login_required
def get_token():
    print(current_user.get_auth_token())
    return dict(token=current_user.get_auth_token())
