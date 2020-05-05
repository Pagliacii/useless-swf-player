#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
Created Date:       2020-04-30 12:05:07
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-04-30 18:48:12
Copyright © 2020-Pagliacii-MIT License
"""

import logging
from loguru import logger


class InterceptHandler(logging.Handler):
    """Create a custom handler that using the loguru logger"""
    def emit(self, record):
        # Retrieve context where the logging call occurred,
        # this happens to be in the 6th frame upward
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


handler = InterceptHandler()
