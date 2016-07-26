#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Export command module
'''
# Imports

# Built-in dependencies

import sys

# Package dependencies

from dtb.commands import CliParser
from dtb.databases import Database
from dtb.formats import FormatRepository

# Module metadata

__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT'
__version__ = '1.0-dev'
__usage__ = '%(prog)s -b BASE -f FORMAT [-m] [-o FILENAME]'
__epilog__ = 'Report bugs and feature requests to {}.' \
    .format('https://github.com/paulofreitas/dtb-ibge/issues')

# Classes


class TerritorialDataExporter(CliParser):
    '''Territorial data exporter command.'''

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
                         choices=FormatRepository.findExportableFormatNames(),
                         help='Format to export the database.\n'
                             + 'Options: %(choices)s')
        self.addArgument('export',
                         '-m', '--minify',
                         dest='minified',
                         action='store_true',
                         help='Minifies output file whenever possible.')
        self.addArgument('export',
                         '-o', '--out',
                         dest='filename',
                         nargs='?',
                         help='Specify a file to write the export to.\n'
                             + 'If none are specified, %(prog)s writes data to standard output.')

    def parse(self):
        '''Parses the given command line arguments.'''
        args = super(self.__class__, self).parse()

        if not args.base:
            self._parser.error(
                'You need to give the database year you want to export.')

        if not args.format:
            self._parser.error(
                'You need to give the database format you want to export.')

        try:
            base = Database(args.base, self._logger)
            base.retrieve().parse() \
                .export(args.format, args.minified, args.filename)
        except KeyboardInterrupt:
            self._logger.info('> Exporting was canceled.')
        except Exception as e:
            sys.stderr.write(
                'EXCEPTION CAUGHT: {}: {}\n'.format(type(e).__name__, e.message)
            )
            sys.exit(1)


if __name__ == '__main__':
    TerritorialDataExporter().parse()
