#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Brazilian territorial distribution data builder

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
# -- Metadata -----------------------------------------------------------------

__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT'
__version__ = '1.0-dev'
__usage__ = '%(prog)s -b BASE -f FORMAT [-m] [-o FILENAME]'
__epilog__ =\
    'Report bugs and feature requests to https://github.com/paulofreitas/dtb-ibge/issues.'

BASES = [2003, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]
RAW_FORMATS = ['csv', 'json', 'php', 'plist', 'sql', 'sqlite3', 'xml', 'yaml']
MINIFIABLE_FORMATS = ['csv', 'json', 'plist', 'sql', 'xml', 'yaml']

# -- Imports ------------------------------------------------------------------

# Built-in modules

import os

# Package modules

from core.entities import TerritorialBase
from core.helpers import CliParser

# -- Implementation -----------------------------------------------------------

class TerritorialDataBuilder(CliParser):
    def configure(self):
        self.addArgumentGroup('build', 'Build options')
        self.addArgument('build',
                         '-b', '--bases',
                         metavar='BASE',
                         nargs='*',
                         default=BASES,
                         help='Database years to build.\n' \
                             + 'Defaults to all available: {}' \
                                 .format(', '.join(map(str, BASES))))
        self.addArgument('build',
                         '-r', '--raw',
                         metavar='FORMAT',
                         nargs='*',
                         default=RAW_FORMATS,
                         help='Raw formats to build the database.\n' \
                             + 'Defaults to all available: {}' \
                                 .format(', '.join(RAW_FORMATS)))
        self.addArgument('build',
                         '-m', '--min',
                         metavar='FORMAT',
                         nargs='*',
                         default=MINIFIABLE_FORMATS,
                         help='Minifiable formats to build the database.\n' \
                             + 'Defaults to all available: {}' \
                                 .format(', '.join(MINIFIABLE_FORMATS)))

    def parse(self):
        args = super(self.__class__, self).parse()

        base_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

        try:
            for base in map(str, args.bases):
                raw_dir = os.path.join(base_dir, 'data', base)
                minified_dir = os.path.join(base_dir, 'data', 'minified', base)

                self._logger.info('> Building {} base...'.format(base))

                try:
                    os.makedirs(raw_dir)
                    os.makedirs(minified_dir)
                except:
                    pass

                os.chdir(raw_dir)
                base_data = TerritorialBase(base, self._logger).retrieve().parse()

                for raw_format in args.raw:
                    base_data.export(raw_format, False, 'auto')

                os.chdir(minified_dir)

                for minifiable_format in args.min:
                    base_data.export(minifiable_format, True, 'auto')
        except KeyboardInterrupt as e:
            self._logger.info('> Building was canceled.')


if __name__ == '__main__':
    TerritorialDataBuilder().parse()
