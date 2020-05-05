#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
Created Date:       2020-04-29 23:41:37
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-05-02 22:21:00
Copyright © 2020-Pagliacii-MIT License
"""

import json

from app import db
from app.errors import FieldLacked, NotExpected


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, unique=True)
    created_time = db.Column(db.String(64))
    accessed_time = db.Column(db.String(64))
    path = db.Column(db.String(256))

    def __repr__(self):
        return f"<File-{self.id}-{self.name}>"

    @classmethod
    def from_file_info(cls, file_info):
        if not isinstance(file_info, dict):
            raise NotExpected("file_info", "dict", type(file_info))

        if "name" not in file_info:
            raise FieldLacked("name")

        if "created_time" not in file_info:
            raise FieldLacked("created_time")

        if "accessed_time" not in file_info:
            raise FieldLacked("accessed_time")

        if "path" not in file_info:
            raise FieldLacked("path")

        return cls(
            name=file_info["name"],
            created_time=file_info["created_time"],
            accessed_time=file_info["accessed_time"],
            path=file_info["path"],
        )

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "created_time": self.created_time,
            "accessed_time": self.accessed_time,
            "path": self.path
        })
