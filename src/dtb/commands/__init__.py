#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Commands package

This package provides a base command class and concrete command modules.
'''
# Imports

# Built-in dependencies

import argparse
import logging
import sys

# Package dependencies

from dtb.core.types import AbstractClass

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT License'

# Classes


class Command(AbstractClass):
    '''Abstract command class.'''

    def __init__(self):
        '''Constructor.'''
        self._parser = argparse.ArgumentParser(usage=self.usage,
                                               description=self.description,
                                               epilog=self.epilog)
        self._parser.conflict_handler = 'resolve'
        self._parser.formatter_class = argparse.RawTextHelpFormatter
        self._arguments = {}

        self.setDefaults()
        self.setLogging()

    def addArgumentGroup(self, key, name):
        '''Adds a new argument group.'''
        self._arguments[key] = self._parser.add_argument_group(name)

    def addArgument(self, group, *args, **kwargs):
        '''Adds a new argument to the given group.'''
        self._arguments[group].add_argument(*args, **kwargs)

    def setDefaults(self):
        '''Sets the command default arguments.'''
        self.addArgumentGroup('global', 'Global options')
        self.addArgument('global',
                         '-h', '--help',
                         action='help',
                         help='Display this information')
        self.addArgument('global',
                         '-v', '--version',
                         action='version',
                         version='%(prog)s ' + self.version,
                         help='Show version information and exit')
        self.addArgument('global',
                         '-V', '--verbose',
                         action='store_true',
                         help='Display informational messages and warnings')

    def setLogging(self):
        '''Sets the command logging handlers.'''
        # Setup stream handler
        stream_formatter = logging.Formatter('%(message)s')
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(stream_formatter)

        self._logger = logging.getLogger('dtb')
        self._logger.addHandler(stream_handler)
        self._logger.setLevel(logging.INFO)

    @property
    def usage(self):
        '''Defines the command usage syntax.'''
        return None

    @property
    def description(self):
        '''Defines the command description.'''
        return None

    @property
    def epilog(self):
        '''Defines the command epilog message.'''
        return None

    @property
    def version(self):
        '''Defines the command version.'''
        return __version__

    def configure(self):
        '''Configures the command arguments.'''
        raise NotImplementedError

    def parse(self):
        '''Parses the given command arguments.'''
        self.configure()

        args = self._parser.parse_args()

        if args.verbose:
            self._logger.setLevel(logging.DEBUG)

        return args

    def run(self):
        '''Runs the command.'''
        raise NotImplementedError
