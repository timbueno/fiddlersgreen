# -*- coding: utf-8 -*-
"""
    fiddlersgreen.settings
    ~~~~~~~~~~~~~~~~~

    fiddlersgreen settings module

"""
import os


os_env = os.environ


class Config(object):
    """Base Configuration"""
    APP_ENV = 'base'
    SECRET_KEY = os_env.get('SECRET_KEY', 'secret-key')
    DEBUG = False
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class DevConfig(Config):
    """Development Configuration"""
    APP_ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    # Put the db file in the project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_NAME)


class TestConfig(Config):
    """Testing Configuration"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'


config = {
    'dev': DevConfig,
    'test': TestConfig,

    'default': DevConfig
}
