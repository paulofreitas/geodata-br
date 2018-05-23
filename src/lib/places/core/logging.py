#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Core logging module
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

import logging
import sys

# Classes


class Logger(object):
    '''Base logger class.'''

    @staticmethod
    def instance(name=None, level=logging.NOTSET):
        '''Returns a logger instance.

        Arguments:
            name (str): The logger name
            level (int): The logger level

        Returns:
            logging.Logger: The requested logger instance
        '''
        logger = logging.getLogger(name)
        logger.setLevel(level)

        return logger

    @staticmethod
    def setup(verbose=False, filename=None):
        '''Setups the root logger.

        Arguments:
            verbose (bool): Whether or not the logger should be verbose
            filename (string): A file to log errors
        '''
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
