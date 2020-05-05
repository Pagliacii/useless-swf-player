#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
Created Date:       2020-04-30 11:24:23
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-05-02 15:43:07
Copyright © 2020-Pagliacii-MIT License
"""


class Error(Exception):
    """Base class for exceptions in this app."""
    pass


class NotExpected(Error):
    """Raised when the argument type isn't expected

    Args:

        argument (str): the argument name
        expected (str): expected argument type
        actual (:obj: `type`): actual type

    Attributes:

        argument_name (str): the argument name
        expected_type (str): expected argument type
        actual_type (:obj: `type`): actual type
        message (str): error message
    """
    def __init__(self, argument, expected, actual):
        self.argument_name = argument
        self.expected_type = expected
        self.actual_type = actual
        self.message = (
            f"The argument {argument} expects a {expected} type, got {actual}."
        )
        super().__init__(self.message)


class FieldLacked(Error):
    """Raised when the specific field is lacked

    Args:

        field (str): field name

    Attributes:

        field (str): the specific field
        message (str): error message
    """
    def __init__(self, field):
        self.field = field
        self.message = f"The specific field {field} is lacked."
        super().__init__(self.message)


class InvalidHeader(Error):
    """Raised when the header of swf file is invalid"""
    pass
