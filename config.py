#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
Created Date:       2020-04-29 18:07:56
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-04-30 12:12:08
Copyright © 2020-Pagliacii-MIT License
"""

import os

root_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "how-can-you-guess-this"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or
        f"sqlite:///{os.path.join(root_dir, 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGFILE = os.path.join(root_dir, "app.log")


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    LOG_BACKTRACE = True
    LOG_LEVEL = 'DEBUG'


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    LOG_BACKTRACE = False
    LOG_LEVEL = 'INFO'
