#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Export command module
'''
# Imports

# Package dependencies

from geodatabr.commands import Command
from geodatabr.core.i18n import Translator
from geodatabr.core.logging import logger
from geodatabr.encoders import EncoderFactory, EncoderFormatRepository

# Classes


class DatasetExporterCommand(Command):
    '''
    The dataset exporter command.
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
        return 'Exports the dataset'

    @property
    def usage(self):
        '''
        Defines the command usage syntax.
        '''
        return '%(prog)s -f FORMAT [-l LOCALE] [-o FILENAME]'

    def configure(self):
        '''
        Defines the command arguments.
        '''
        locales = Translator.locales()

        self.addArgument('-f', '--format',
                         metavar='FORMAT',
                         choices=EncoderFormatRepository.listNames(),
                         help=('File format to export the dataset.\n'
                               'Options: %(choices)s'))
        self.addArgument('-l', '--locale',
                         metavar='LOCALE',
                         choices=locales,
                         default='en',
                         help=('Locale to export the dataset.\n'
                               'Options: %(choices)s\n'
                               'Default: %(default)s'))
        self.addArgument('-o', '--out',
                         dest='filename',
                         nargs='?',
                         help=('Filename to write the export to.\n'
                               'If none are specified, %(prog)s writes data to '
                               'standard output.'))

    def handle(self, args):
        '''
        Handles the command.

        Raises:
            geodatabr.encoders.EncodeError: When dataset fails to encode
        '''
        if not args.format:
            self._parser.error(
                'You need to give the output format you want to export.')

        Translator.locale = args.locale

        try:
            encoder = EncoderFactory.fromFormat(args.format)
            encoder.encodeToFile(args.filename)
        except KeyboardInterrupt:
            logger().info('> Exporting was canceled.')
