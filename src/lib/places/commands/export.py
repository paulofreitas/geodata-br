#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Export command module
'''
# Imports

# Package dependencies

from places.commands import Command
from places.core.logging import Logger
from places.databases import DatabaseFactory
from places.formats import FormatRepository

# Module logging

logger = Logger.instance(__name__)

# Classes


class DatabaseExporterCommand(Command):
    '''
    The database exporter command.
    '''

    @property
    def name(self):
        '''
        Defines the command name.
        '''
        return 'export'

    @property
    def description(self):
        '''
        Defines the command description.
        '''
        return 'Exports a database'

    @property
    def usage(self):
        '''
        Defines the command usage syntax.
        '''
        return '%(prog)s -b BASE -f FORMAT [-m] [-o FILENAME]'

    def configure(self):
        '''
        Defines the command arguments.
        '''
        self.addArgument('-b', '--base',
                         help='Database year to export.')
        self.addArgument('-f', '--format',
                         metavar='FORMAT',
                         choices=FormatRepository.listExportableFormatNames(),
                         help=('Format to export the database.\n'
                               'Options: %(choices)s'))
        self.addArgument('-m', '--minify',
                         dest='minify',
                         action='store_true',
                         help='Minifies output file whenever possible.')
        self.addArgument('-o', '--out',
                         dest='filename',
                         nargs='?',
                         help=('Specify a file to write the export to.\n'
                               'If none are specified, %(prog)s writes data to '
                               'standard output.'))

    def handle(self, args):
        '''
        Handles the command.
        '''
        if not args.base:
            self._parser.error(
                'You need to give the database year you want to export.')

        if not args.format:
            self._parser.error(
                'You need to give the database format you want to export.')

        try:
            base = DatabaseFactory.fromYear(args.base)
            base.parse().export(args.format, args.filename, minify=args.minify)
        except KeyboardInterrupt:
            logger.info('> Exporting was canceled.')
