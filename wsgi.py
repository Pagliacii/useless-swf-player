#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
Created Date:       2020-04-29 18:14:20
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-05-04 23:48:21
Copyright © 2020-Pagliacii-MIT License
"""

import datetime
import time

from flask import g, request
from loguru import logger
from rfc3339 import rfc3339

from app import create_app, db
from app.models import File

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'File': File}


@app.before_request
def start_timer():
    g.start = time.time()


@app.after_request
def log_request(response):
    if request.path == "/favicon.ico":
        return response
    elif request.path.startswith("/static"):
        return response

    now = time.time()
    duration = round(now - g.start, 2)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = rfc3339(dt, utc=True)

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    host = request.host.split(":", 1)[0]
    args = dict(request.args)

    log_params = [
        ('method', request.method),
        ('path', request.path),
        ('status', response.status_code),
        ('duration', duration),
        ('time', timestamp),
        ('ip', ip),
        ('host', host),
        ('params', args)
    ]

    request_id = request.headers.get("X-Request-ID")
    if request_id:
        log_params.append(('request_id', request_id))

    parts = []
    for name, value in log_params:
        part = f"{name}={value}"
        parts.append(part)
    line = " ".join(parts)

    logger.debug(line)

    return response


if __name__ == "__main__":
    app.run()
