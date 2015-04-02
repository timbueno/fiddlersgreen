# -*- coding: utf-8 -*-
"""
    fiddlersgreen.frontend.auth.views
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Authentication Views

"""
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user

from ...models import User
from ...core import login_manager
from .. import route
from . import bp
from .forms import LoginForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.token_loader
def load_user_from_token(token):
    return User.verify_auth_token(token)


@route(bp, '/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or
                            url_for('public.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)
