#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
Created Date:       2020-04-28 18:35:58
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-05-03 14:42:06
Copyright © 2020-Pagliacii-MIT License
"""

import json
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from loguru import logger

db = SQLAlchemy()
migrate = Migrate()


def create_app(mode="production"):
    app = Flask(
        __name__,
        instance_relative_config=False,
        static_folder="../static",
        template_folder="../templates"
    )
    if mode == "development":
        app.config.from_object("config.DevConfig")
    else:
        app.config.from_object("config.ProdConfig")

    db.init_app(app)
    migrate.init_app(app, db)

    # logging properties are defined in config.py
    logger.start(
        app.config["LOGFILE"],
        colorize=True,
        level=app.config["LOG_LEVEL"],
        format="{time} {level} {message}",
        backtrace=app.config["LOG_BACKTRACE"],
        rotation="25 MB"
    )
    # register loguru as handler
    from app.logging import handler
    app.logger.addHandler(handler)

    with app.app_context():
        db.create_all()
        from app.utils import scan_swfs_folder
        scan_swfs_folder(db, logger)

        # Include our blueprints
        from . import files, route, video
        # Register Blueprints
        app.register_blueprint(files.bp)
        app.register_blueprint(route.bp)
        app.register_blueprint(video.bp)

    return app
