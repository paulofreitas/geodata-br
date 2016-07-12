#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Brazilian territorial distribution data

The MIT License (MIT)

Copyright (c) 2013-2016 Paulo Freitas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
# -- Imports ------------------------------------------------------------------

# Built-in modules

import argparse
import logging
import sys

# -- Implementation -----------------------------------------------------------


class CliParser(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(
            description=globals().get('__doc__'),
            usage=globals().get('__usage__'),
            epilog=globals().get('__epilog__'),
            conflict_handler='resolve',
            formatter_class=argparse.RawTextHelpFormatter
        )
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
                         version='%(prog)s ' + globals().get('__version__', ''),
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


class Struct(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    def copy(self):
        return Struct(dict.copy(self))
