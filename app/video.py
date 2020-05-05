#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
Created Date:       2020-04-29 18:13:18
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-05-03 14:19:10
Copyright © 2020-Pagliacii-MIT License
"""

from flask import abort, Blueprint, render_template

from app.models import File
from app.swf_parser import Header

# Set up a Blueprint
bp = Blueprint("video", __name__, url_prefix="/video")


@bp.route("/<int:file_id>", methods=["GET"])
def video(file_id):
    if (file_data := File.query.filter_by(id=file_id).first()) is None:
        abort(404)

    file_header = Header(file_data.path)
    data = {
        "frame": {
            "width": file_header.frame_width,
            "height": file_header.frame_height,
        },
        "name": file_data.name,
    }
    return render_template("video.html", data=data)
