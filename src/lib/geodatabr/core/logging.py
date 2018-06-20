#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Core logging module."""
from __future__ import absolute_import

# Imports

# Built-in dependencies

import inspect
import logging
from logging import Logger as BaseLogger
import sys

# Classes


class Logger(object):
    """Base logger class."""

    @staticmethod
    def instance(name: str = None, level: int = logging.NOTSET) -> BaseLogger:
        """
        Returns a logger instance.

        Args:
            name: The logger name
            level: The logger level

        Returns:
            The requested logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        return logger

    @staticmethod
    def setup(verbose: bool = False, filename: str = None):
        """
        Setups the root logger.

        Args:
            verbose: Whether or not the logger should be verbose
            filename: A file to log errors
        """
        logging_level = logging.DEBUG if verbose else logging.INFO
        logger = Logger.instance(level=logging_level)

        # Setup the stream handler
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        logger.addHandler(stream_handler)

        # Setup the file handler when needed
        if filename:
            file_handler = logging.FileHandler(filename)
            file_handler.setLevel(logging.ERROR)
            logger.addHandler(file_handler)


# Functions


def logger(level: int = logging.NOTSET) -> BaseLogger:
    """
    Logger factory method.

    Args:
        level: The logger level

    Returns:
        A module-level logger instance
    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])

    return Logger.instance(module.__name__ if module else None, level)
