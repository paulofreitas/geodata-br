#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
CLI package

This package provides a base CLI argument parser class and concrete command
modules.
'''
# Imports

# Built-in dependencies

import argparse
import logging
import sys

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT License'

# Classes


class CliParser(object):
    def __init__(self, **metadata):
        self._metadata = metadata
        self._parser = argparse.ArgumentParser(**metadata)
        self._parser.conflict_handler = 'resolve'
        self._parser.formatter_class = argparse.RawTextHelpFormatter
        self._arguments = {}

        self.setDefaults()
        self.setLogging()

    def addArgumentGroup(self, key, name):
        self._arguments[key] = self._parser.add_argument_group(name)

    def addArgument(self, group, *args, **kwargs):
        self._arguments[group].add_argument(*args, **kwargs)

    def setDefaults(self):
        self.addArgumentGroup('global', 'Global options')
        self.addArgument('global',
                         '-h', '--help',
                         action='help',
                         help='Display this information'
        )
        self.addArgument('global',
                         '-v', '--version',
                         action='version',
                         version='%(prog)s ' + self._metadata.get('__version__', ''),
                         help='Show version information and exit'
        )
        self.addArgument('global',
                         '-V', '--verbose',
                         action='store_true',
                         help='Display informational messages and warnings'
        )

    def setLogging(self):
        # Setup stream handler
        stream_formatter = logging.Formatter('%(message)s')
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(stream_formatter)

        self._logger = logging.getLogger('dtb')
        self._logger.addHandler(stream_handler)
        self._logger.setLevel(logging.INFO)

    def configure(self):
        pass

    def parse(self):
        self.configure()

        args = self._parser.parse_args()

        if args.verbose:
            self._logger.setLevel(logging.DEBUG)

        return args
