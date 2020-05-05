#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
Created Date:       2020-04-29 18:13:12
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-05-04 23:53:51
Copyright © 2020-Pagliacii-MIT License
"""

from flask import Blueprint, render_template

from app.models import File


# Set up a Blueprint
bp = Blueprint("route", __name__)


@bp.route("/", methods=["GET"])
def home():
    files = File.query.all()
    if not files:
        files = []

    return render_template("index.html", files=files)


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@bp.app_errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500
