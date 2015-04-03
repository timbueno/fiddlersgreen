# -*- coding: utf-8 -*-
"""
    fiddlersgreen.api.errors
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Api error handlers

"""
from flask import jsonify

from ..compat import text_type


def not_found(message):
    msg = 'URL not found'
    if type(message) is text_type:
        msg = message
    response = jsonify({'error': 'not found', 'message': msg})
    status_code = 404
    return response, status_code


def unauthorized(message):
    msg = 'Invalid Credentials'
    if type(message) is text_type:
        msg = message
    response = jsonify({'error': 'unauthorized', 'message': msg})
    status_code = 401
    response.headers['WWW-Authenticate'] = 'Basic realm="Unauthorized Access"'
    return response, status_code


def bad_request(message):
    msg = 'Bad Request'
    if type(message) is text_type:
        msg = message
    response = jsonify({'error': 'bad request', 'message': msg})
    status_code = 400
    return response, status_code


def forbidden(message):
    msg = 'Forbidden'
    if type(message) is text_type:
        msg = message
    response = jsonify({'error': 'forbidden', 'message': msg})
    status_code = 403
    return response, status_code


def internal_server_error(message):
    msg = 'Internal Server Error'
    if type(message) is text_type:
        msg = message
    response = jsonify({'error': 'internal server error', 'message': msg})
    status_code = 500
    return response, status_code
