#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
Created Date:       2020-04-29 18:21:41
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-05-10 00:26:01
Copyright © 2020-Pagliacii-MIT License
"""

import os

from flask import abort, Blueprint, jsonify, request, Response, stream_with_context
from loguru import logger
from werkzeug.utils import secure_filename

from app import db
from app.models import File
from app.utils import scan_swfs_folder, get_file_accessed_time

from flask import current_app as app

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
            logger.error("Rename failed, because the new filename is empty")
            return jsonify({"status": "failure", "reason": "no new filename"}), 400  # noqa E501
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


def valid_file_extension(filename: str) -> bool:
    if "." not in filename:
        return False
    return filename.rsplit(".", 1)[1].upper() in app.config["ALLOWED_FILE_EXTENSIONS"]  # noqa E501


def valid_filesize(filesize: int) -> bool:
    return int(filesize) <= app.config["MAX_FILESIZE"]


def gen_filename(filename: str) -> str:
    """
    If filename was exist already, return a new name
    """
    i = 1
    while os.path.exists(os.path.join(app.config["FILE_UPLOADS"], filename)):
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{str(i)}{ext}"
        i += 1
    return filename


@bp.route("/upload", methods=["POST"])
def upload_new_file():
    if request.files:

        # 1. check file size in cookies
        file_size = request.cookies.get("filesize", 0)
        if not valid_filesize(file_size):
            reason = "Filesize exceeded maximum limit"
            logger.warning(reason)
            return jsonify({"status": "failure", "reason": reason}), 400

        file_uploads = request.files["files[]"]
        # 2. check filename
        if file_uploads.filename == "":
            reason = "No filename"
            logger.warning(reason)
            return jsonify({"status": "failure", "reason": reason}), 400
        if not valid_file_extension(file_uploads.filename):
            reason = "That file extension is not allowed"
            logger.warning(reason)
            return jsonify({"status": "failure", "reason": reason}), 415

        logger.debug(f"file: {file_uploads}, filesize: {file_size}")
        filename = secure_filename(file_uploads.filename)
        filename = gen_filename(filename)
        file_uploads.save(os.path.join(app.config["FILE_UPLOADS"], filename))
        logger.debug(f"file: {file_uploads.filename} saved as {filename}")
        return jsonify({"status": "ok"})

    logger.info("There hasn't upload files")
    return jsonify({"status": "failure", "reason": "No file uploaded"})
