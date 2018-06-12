#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Build command module
'''
# Imports

# Package dependencies

from geodatabr.commands import Command
from geodatabr.core.constants import DATA_DIR
from geodatabr.core.helpers.documentation import ProjectReadme, DatasetReadme
from geodatabr.core.helpers.filesystem import File
from geodatabr.core.i18n import Translator
from geodatabr.core.logging import Logger
from geodatabr.exporters import ExporterFactory
from geodatabr.formats import FormatRepository

# Module logging

logger = Logger.instance(__name__)

# Classes


class BuildCommand(Command):
    '''
    A command class to build the dataset files.
    '''

    @property
    def name(self):
        '''
        Defines the command name.
        '''
        return 'build'

    @property
    def description(self):
        '''
        Defines the command description.
        '''
        return 'Build the dataset files'

    @property
    def usage(self):
        '''
        Defines the command usage syntax.
        '''
        return '%(prog)s [-l LOCALE] [-f FORMAT]'

    def configure(self):
        '''
        Defines the command arguments.
        '''
        locales = Translator.locales()
        formats = FormatRepository.listExportableFormatNames()

        self.addArgument('-l', '--locales',
                         metavar='LOCALE',
                         nargs='*',
                         default=locales,
                         help=('Locales to build the dataset.\n'
                               'Defaults to all available: {}' \
                                   .format(', '.join(locales))))
        self.addArgument('-f', '--formats',
                         metavar='FORMAT',
                         nargs='*',
                         default=formats,
                         help=('Formats to build the dataset.\n'
                               'Defaults to all available: {}' \
                                    .format(', '.join(formats))))

    def handle(self, args):
        '''
        Handles the command.
        '''
        try:
            for locale in args.locales:
                Translator.locale = locale

                logger.info('> Building locale: %s', locale)

                dataset_dir = DATA_DIR / locale
                dataset_dir.create(parents=True)

                with dataset_dir:
                    for dataset_format in args.formats:
                        exporter = ExporterFactory.fromFormat(dataset_format)
                        exporter.exportToFile()

                    logger.info('Generating dataset README file...')

                    DatasetReadme(dataset_dir).write()

            logger.info('Generating project README file...')

            ProjectReadme().write()
        except KeyboardInterrupt:
            logger.info('Building was canceled.')
