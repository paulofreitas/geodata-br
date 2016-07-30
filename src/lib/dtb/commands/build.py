#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Build command module
'''
# Imports

# Built-in dependencies

from os import chdir, makedirs
from os.path import join as path

# Package dependencies

from dtb.commands import Command
from dtb.core.constants import DATA_DIR
from dtb.databases import Database
from dtb.formats import FormatRepository

# Classes


class DatabaseBuilderCommand(Command):
    '''The database builder command.'''

    @property
    def name(self):
        '''Defines the command name.'''
        return 'build'

    @property
    def description(self):
        '''Defines the command description.'''
        return 'Builds a database'

    @property
    def usage(self):
        '''Defines the command usage syntax.'''
        return '%(prog)s -b BASE -r FORMAT -m FORMAT'

    def configure(self):
        '''Defines the command arguments.'''
        bases = Database.bases
        raw_formats = FormatRepository.findExportableFormatNames()
        minifiable_formats = FormatRepository.findMinifiableFormatNames()

        self.addArgument('-b', '--bases',
                         metavar='BASE',
                         nargs='*',
                         default=bases,
                         help=('Database years to build.\n'
                               'Defaults to all available: {}' \
                                   .format(', '.join(bases))))
        self.addArgument('-r', '--raw',
                         metavar='FORMAT',
                         nargs='*',
                         default=raw_formats,
                         help=('Raw formats to build the database.\n'
                               'Defaults to all available: {}' \
                                    .format(', '.join(raw_formats))))
        self.addArgument('-m', '--min',
                         metavar='FORMAT',
                         nargs='*',
                         default=minifiable_formats,
                         help=('Minifiable formats to build the database.\n'
                               'Defaults to all available: {}' \
                                   .format(', '.join(minifiable_formats))))

    def handle(self, args):
        '''Handles the command.'''
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
                base_data = Database(base, self._logger).parse()

                for raw_format in args.raw:
                    base_data.export(raw_format, False, 'auto')

                chdir(minified_dir)

                for minifiable_format in args.min:
                    base_data.export(minifiable_format, True, 'auto')
        except KeyboardInterrupt:
            self._logger.info('> Building was canceled.')
