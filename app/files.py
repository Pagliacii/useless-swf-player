#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
Created Date:       2020-04-29 18:21:41
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-05-04 00:51:43
Copyright © 2020-Pagliacii-MIT License
"""

import os

from flask import abort, Blueprint, jsonify, request, Response, stream_with_context
from loguru import logger

from app import db
from app.models import File
from app.utils import scan_swfs_folder, get_file_accessed_time


# Set up a Blueprint
bp = Blueprint("bp", __name__, url_prefix="/files")


@bp.route("/update", methods=["GET"])
def get_files_info():
    try:
        scan_swfs_folder(db, logger)
    except Exception as e:
        logger.error(f"Scanning swfs folder failed, caused by {e}")
        return jsonify({"status": "failure", "reason": str(e)}), 422

    return jsonify({"status": "ok"})


@bp.route("/<path:file_name>", methods=["GET", "DELETE", "POST"])
def get_file_contents(file_name):
    file_data = File.query.filter_by(name=file_name).first()

    if request.method == "DELETE":
        if not file_data:
            return jsonify({"status": "failure", "reason": "no such file"}), 404  # noqa E501

        try:
            os.remove(file_data.path)
        except Exception as e:
            logger.error(f"Removing {file_data.path} failed, caused by {e}")

        db.session.delete(file_data)
        db.session.commit()
        return jsonify({"status": "ok"})

    if request.method == "POST":
        new_name = request.form.get("filename")
        logger.debug(f'Renaming: "{file_name}" => "{new_name}"')
        if not new_name:
            logger.error("Rename failed, because the new filenam is empty")
            return jsonify({"status": "failure", "reason": "no new filename"}), 422  # noqa E501
        if File.query.filter_by(name=new_name).first():
            logger.error("Rename failed, because the new filename already exists")  # noqa E501
            return jsonify({"status": "failure", "reason": "Filename existed"}), 400  # noqa E501

        new_path = os.path.join(os.path.dirname(file_data.path), new_name)
        try:
            os.rename(file_data.path, new_path)
        except Exception as e:
            logger.error(f"Rename local file failed, caused by {e}")
            return jsonify({"status": "failure", "reason": str(e)}), 422

        file_data.name = new_name
        file_data.path = new_path
        file_data.accessed_time = get_file_accessed_time(os.stat(new_path))
        db.session.commit()
        return jsonify({"status": "ok"})

    if not file_data:
        abort(404)
    if not os.path.isfile(file_data.path):
        abort(404)

    def file_contents():
        with open(file_data.path, "rb") as f:
            for line in f:
                yield line

    return Response(
        stream_with_context(file_contents()),
        mimetype="application/x-shockwave-flash"
    )
