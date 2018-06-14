#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Encode command module."""
# Imports

# Built-in dependencies

from argparse import Namespace

# Package dependencies

from geodatabr.commands import Command
from geodatabr.core.i18n import Translator
from geodatabr.core.logging import logger
from geodatabr.encoders import EncoderFactory, EncoderFormatRepository, \
    EncodeError

# Classes


class EncodeCommand(Command):
    """A command class to encode the dataset."""

    @property
    def name(self) -> str:
        """Gets the command name."""
        return 'encode'

    @property
    def description(self) -> str:
        """Gets the command description."""
        return 'Encode the dataset'

    @property
    def usage(self) -> str:
        """Gets the command usage syntax."""
        return '%(prog)s -f FORMAT [-l LOCALE] [-o FILENAME]'

    def configure(self):
        """Defines the command arguments."""
        self.addArgument('-f', '--format',
                         metavar='FORMAT',
                         choices=EncoderFormatRepository.listNames(),
                         help=('File format to encode the dataset.\n'
                               'Options: %(choices)s'))
        self.addArgument('-l', '--locale',
                         metavar='LOCALE',
                         choices=Translator.locales(),
                         default='en',
                         help=('Locale to encode the dataset.\n'
                               'Options: %(choices)s\n'
                               'Default: %(default)s'))
        self.addArgument('-o', '--out',
                         dest='filename',
                         nargs='?',
                         help=('Filename to save the dataset.\n'
                               'If none are specified, data is written to '
                               'standard output.'))

    def handle(self, args: Namespace):
        """Handles the command."""
        if not args.format:
            self._parser.error(
                'You need to give the output format you want to encode.')

        Translator.locale = args.locale

        try:
            encoder = EncoderFactory.fromFormat(args.format)

            logger().info('Encoding dataset to %s format...',
                          encoder.format().friendlyName)

            serializer = encoder.serializer(**encoder.serializationOptions)
            encoder.encodeToFile(serializer.serialize(), args.filename)
        except EncodeError:
            logger().error('Failed to encode dataset.')
        except KeyboardInterrupt:
            logger().info('Encoding was canceled.')
