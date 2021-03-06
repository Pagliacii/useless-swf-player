#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
Created Date:       2020-04-29 17:27:04
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-05-10 11:00:27
Copyright © 2020-Pagliacii-MIT License
"""

import os
from datetime import datetime


def get_file_created_time(file_path):
    return datetime.fromtimestamp(
        os.path.getctime(file_path), datetime.now().astimezone().tzinfo
    ).isoformat()


def get_file_accessed_time(file_path):
    return datetime.fromtimestamp(
        os.path.getatime(file_path), datetime.now().astimezone().tzinfo
    ).isoformat()


def get_file_info(file_path):
    return {
        "name": os.path.basename(file_path),
        "created_time": get_file_created_time(file_path),
        "accessed_time": get_file_accessed_time(file_path),
        "path": file_path,
    }


def get_files_info(directory):
    directory_path = os.path.abspath(directory)
    if not os.path.isdir(directory_path):
        raise Exception(f"The argument isn't a directory: {directory=}")

    for filename in os.listdir(directory_path):
        if not filename.endswith(".swf"):
            continue

        file_path = os.path.abspath(os.path.join(directory_path, filename))
        yield get_file_info(file_path)


def scan_swfs_folder(database, logger):
    # List the swfs directory and insert infos to db
    from app.errors import FieldLacked, NotExpected
    from app.models import File

    counter = 0
    directory = os.path.abspath(os.path.join(__file__, '../..', 'swfs'))
    for file_info in get_files_info(directory):
        try:
            new_file = File.from_file_info(file_info)
        except (FieldLacked, NotExpected) as e:
            logger.error(
                f"Get file info from {file_info['file_path']} failed, caused by {e}"  # noqa E501
            )
            continue
        except Exception as e:
            logger.critical(f"Unknown exception: {e}")
            raise

        # Update or insert
        if exists := database.session.query(File).filter_by(name=new_file.name).first():  # noqa E501
            exists.created_time = new_file.created_time
            exists.accessed_time = new_file.accessed_time
            exists.path = new_file.path
            database.session.commit()
        else:
            database.session.add(new_file)

        counter += 1
        if counter > 9:
            database.session.commit()
            counter = 0
    database.session.commit()
