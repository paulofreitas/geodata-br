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

from dtb.commands import Command
from dtb.databases import Database
from dtb.formats import FormatRepository

# Classes


class ExporterCommand(Command):
    '''The database exporter command.'''

    @property
    def usage(self):
        '''Defines the command usage syntax.'''
        return '%(prog)s -b BASE -f FORMAT [-m] [-o FILENAME]'

    @property
    def description(self):
        '''Defines the command description.'''
        return __doc__

    @property
    def epilog(self):
        '''Defines the command epilog message.'''
        return 'Report bugs and feature requests to {}.' \
            .format('https://github.com/paulofreitas/dtb-ibge/issues')

    def configure(self):
        '''Configures the command arguments.'''
        self.addArgumentGroup('export', 'Export options')
        self.addArgument('export',
                         '-b', '--base',
                         help='Database year to export.')
        self.addArgument('export',
                         '-f', '--format',
                         metavar='FORMAT',
                         choices=FormatRepository.findExportableFormatNames(),
                         help=('Format to export the database.\n'
                               'Options: %(choices)s'))
        self.addArgument('export',
                         '-m', '--minify',
                         dest='minified',
                         action='store_true',
                         help='Minifies output file whenever possible.')
        self.addArgument('export',
                         '-o', '--out',
                         dest='filename',
                         nargs='?',
                         help=('Specify a file to write the export to.\n'
                               'If none are specified, %(prog)s writes data to '
                               'standard output.'))

    def run(self):
        '''Runs the command.'''
        args = self.parse()

        if not args.base:
            self._parser.error(
                'You need to give the database year you want to export.')

        if not args.format:
            self._parser.error(
                'You need to give the database format you want to export.')

        try:
            base = Database(args.base, self._logger)
            base.parse().export(args.format, args.minified, args.filename)
        except KeyboardInterrupt:
            self._logger.info('> Exporting was canceled.')
        except Exception as e:
            sys.stderr.write(
                'EXCEPTION CAUGHT: {}: {}\n'.format(type(e).__name__, e.message)
            )
            sys.exit(1)


if __name__ == '__main__':
    ExporterCommand().run()
