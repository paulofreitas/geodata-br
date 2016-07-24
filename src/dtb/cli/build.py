#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Brazilian territorial distribution data exporter

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
# Imports

# Built-in dependencies

from os import chdir, makedirs
from os.path import join as path

# Package dependencies

from dtb.cli.base import CliParser
from dtb.core.entities import TerritorialBase
from dtb.core.helpers import DATA_DIR
from dtb.formats.base import FormatRepository

# Metadata

__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT'
__version__ = '1.0-dev'
__usage__ = '%(prog)s -b BASE -r FORMAT -m FORMAT'
__epilog__ = 'Report bugs and feature requests to {}.' \
    .format('https://github.com/paulofreitas/dtb-ibge/issues')

# Constants

BASES = [2003, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]

# Classes


class TerritorialDataBuilder(CliParser):
    '''Territorial data builder command.'''

    def __init__(self):
        super(self.__class__, self).__init__(description=__doc__,
                                             usage=__usage__,
                                             epilog=__epilog__,
                                             version=__version__)

    def configure(self):
        bases = map(str, BASES)
        raw_formats = map(str, FormatRepository.findAllExportableFormats())
        minifiable_formats = map(str, FormatRepository.findAllMinifiableFormats())

        self.addArgumentGroup('build', 'Build options')
        self.addArgument('build',
                         '-b', '--bases',
                         metavar='BASE',
                         nargs='*',
                         default=bases,
                         help='Database years to build.\n' \
                             + 'Defaults to all available: {}' \
                                 .format(', '.join(bases)))
        self.addArgument('build',
                         '-r', '--raw',
                         metavar='FORMAT',
                         nargs='*',
                         default=raw_formats,
                         help='Raw formats to build the database.\n' \
                             + 'Defaults to all available: {}' \
                                 .format(', '.join(raw_formats)))
        self.addArgument('build',
                         '-m', '--min',
                         metavar='FORMAT',
                         nargs='*',
                         default=minifiable_formats,
                         help='Minifiable formats to build the database.\n' \
                             + 'Defaults to all available: {}' \
                                 .format(', '.join(minifiable_formats)))

    def parse(self):
        '''Parses the given command line arguments.'''
        args = super(self.__class__, self).parse()

        try:
            for base in args.bases:
                raw_dir = path(DATA_DIR, base)
                minified_dir = path(DATA_DIR, 'minified', base)

                self._logger.info('> Building {} base...'.format(base))

                try:
                    makedirs(raw_dir)
                    makedirs(minified_dir)
                except OSError:
                    pass

                chdir(raw_dir)
                base_data = TerritorialBase(base, self._logger) \
                    .retrieve() \
                    .parse()

                for raw_format in args.raw:
                    base_data.export(raw_format, False, 'auto')

                chdir(minified_dir)

                for minifiable_format in args.min:
                    base_data.export(minifiable_format, True, 'auto')
        except KeyboardInterrupt:
            self._logger.info('> Building was canceled.')


if __name__ == '__main__':
    TerritorialDataBuilder().parse()
