#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Build command module
'''
# Imports

# Package dependencies

import places.databases.entities

from places.commands import Command
from places.core.constants import DATA_DIR
from places.core.i18n import Translator
from places.core.logging import Logger
from places.databases import DatabaseFactory, DatabaseRepository
from places.formats import FormatRepository

# Module logging

logger = Logger.instance(__name__)

# Classes


class DatasetBuilderCommand(Command):
    '''
    The dataset builder command.
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
        return 'Builds a dataset'

    @property
    def usage(self):
        '''
        Defines the command usage syntax.
        '''
        return '%(prog)s -d DATASET -r FORMAT -m FORMAT'

    def configure(self):
        '''
        Defines the command arguments.
        '''
        datasets = DatabaseRepository.listYears()
        locales = Translator.locales()
        raw_formats = FormatRepository.listExportableFormatNames()
        minifiable_formats = FormatRepository.listMinifiableFormatNames()

        self.addArgument('-d', '--datasets',
                         metavar='DATASET',
                         nargs='*',
                         default=datasets,
                         help=('Datasets to build.\n'
                               'Defaults to all available: {}' \
                                   .format(', '.join(datasets))))
        self.addArgument('-l', '--locales',
                         metavar='LOCALE',
                         nargs='*',
                         default=locales,
                         help=('Locales to build.\n'
                               'Defaults to all available: {}' \
                                   .format(', '.join(locales))))
        self.addArgument('-r', '--raw',
                         metavar='FORMAT',
                         nargs='*',
                         default=raw_formats,
                         help=('Raw formats to build the dataset.\n'
                               'Defaults to all available: {}' \
                                    .format(', '.join(raw_formats))))
        self.addArgument('-m', '--min',
                         metavar='FORMAT',
                         nargs='*',
                         default=minifiable_formats,
                         help=('Minifiable formats to build the dataset.\n'
                               'Defaults to all available: {}' \
                                   .format(', '.join(minifiable_formats))))

    def handle(self, args):
        '''
        Handles the command.
        '''
        try:
            for locale in args.locales:
                Translator.locale = locale

                logger.info('> Building locale: %s', locale)

                for dataset in args.datasets:
                    dataset_dir = DATA_DIR / locale / dataset
                    dataset_dir.create(parents=True)

                    logger.info('> Building dataset: %s', dataset)

                    data = DatabaseFactory.fromYear(dataset).parse()

                    with dataset_dir:
                        for raw_format in args.raw:
                            data.export(raw_format, 'auto')

                        for minifiable_format in args.min:
                            data.export(minifiable_format, 'auto', minify=True)
        except KeyboardInterrupt:
            logger.info('> Building was canceled.')
