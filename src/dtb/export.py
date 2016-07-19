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
# -- Metadata -----------------------------------------------------------------

__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT'
__version__ = '1.0-dev'
__usage__ = '%(prog)s -b BASE -f FORMAT [-m] [-o FILENAME]'
__epilog__ =\
    'Report bugs and feature requests to https://github.com/paulofreitas/dtb-ibge/issues.'

# -- Imports ------------------------------------------------------------------

# Built-in modules

import argparse
import sys

# Package modules

from dtb.core.entities import TerritorialBase, TerritorialData
from dtb.core.helpers import CliParser
from dtb.exporters import FORMATS

# -- Implementation -----------------------------------------------------------


class TerritorialDataExporter(CliParser):
    def __init__(self):
        super(self.__class__, self).__init__(description=__doc__,
                                             usage=__usage__,
                                             epilog=__epilog__,
                                             version=__version__)

    def configure(self):
        self.addArgumentGroup('export', 'Export options')
        self.addArgument('export',
                         '-b', '--base',
                         help='Database year to export.')
        self.addArgument('export',
                         '-f', '--format',
                         metavar='FORMAT',
                         choices=FORMATS.keys(),
                         help='Format to export the database.\nOptions: %(choices)s')
        self.addArgument('export',
                         '-m', '--minify',
                         dest='minified',
                         action='store_true',
                         help='Minifies output file whenever possible.')
        self.addArgument('export',
                         '-o', '--out',
                         dest='filename',
                         nargs='?',
                         const='auto',
                         help='Specify a file to write the export to.\n'
                             + 'If none are specified, %(prog)s writes data to standard output.')

    def parse(self):
        args = super(self.__class__, self).parse()

        if not args.base:
            parser.error('You need to give the database year you want to export.')

        if not args.format:
            parser.error('You need to give the database format you want to export.')

        try:
            base = TerritorialBase(args.base, self._logger)
            base.retrieve().parse() \
                .export(args.format, args.minified, args.filename)
        except KeyboardInterrupt as e:
            self._logger.info('> Exporting was canceled.')
        except Exception as e:
            sys.stderr.write(
                'EXCEPTION CAUGHT: {}: {}\n'.format(type(e).__name__, e.message)
            )
            sys.exit(1)


if __name__ == '__main__':
    TerritorialDataExporter().parse()
