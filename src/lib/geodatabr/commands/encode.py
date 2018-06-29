#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Encode command module."""
# Imports

# Built-in dependencies

import argparse

# Package dependencies

from geodatabr.core import commands, encoders, i18n, logging
from geodatabr.core.utils import io
from geodatabr.dataset import schema, serializers

# Classes


class EncodeCommand(commands.Command):
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
        return '%(prog)s -f FORMAT [-l LOCALE] [-t TABLES]'

    def configure(self):
        """Defines the command arguments."""
        self.addArgument('-f', '--format',
                         metavar='FORMAT',
                         choices=encoders.EncoderFormatRepository.listNames(),
                         help=('File format to encode the dataset.\n'
                               'Options: %(choices)s'))
        self.addArgument('-l', '--locale',
                         metavar='LOCALE',
                         choices=i18n.Translator.locales(),
                         default='en',
                         help=('Locale to encode the dataset.\n'
                               'Options: %(choices)s\n'
                               'Default: %(default)s'))
        self.addArgument('-t', '--tables',
                         metavar='TABLES',
                         nargs='*',
                         choices=schema.TABLES,
                         default=schema.TABLES,
                         help=('Dataset tables to encode.\n'
                               'Options: %(choices)s\n'
                               'Default: All tables'))

    def handle(self, args: argparse.Namespace):
        """Handles the command."""
        if not args.format:
            self._parser.error(
                'You need to give the output format you want to encode.')

        i18n.Translator.locale = args.locale
        logger = logging.logger()

        try:
            encoder = encoders.EncoderFactory.fromFormat(args.format)
            serializer = serializers.Serializer(**encoder.serializationOptions)
            entity_map = dict(zip(schema.TABLES, schema.ENTITIES))

            logger.info('Encoding dataset to %s format...',
                        encoder.format.friendlyName)

            dataset_dir = io.Directory(io.Path.DATA_DIR / args.locale)
            dataset_dir.create(parents=True)

            with dataset_dir:
                if encoder.format.isFlatFile:
                    for table in args.tables:
                        entity = (entity_map.get(table),)
                        encoder.encodeToFile(
                            serializer.serialize(entity).get(table),
                            '{dataset_name}-{table_name}'.format(
                                dataset_name=i18n._('dataset_name'),
                                table_name=table) + encoder.format.extension)

                    self._parser.exit(0)

                encoder.encodeToFile(
                    serializer.serialize(tuple(entity_map.get(table)
                                               for table in args.tables)),
                    i18n._('dataset_name') + encoder.format.extension)
        except encoders.EncodeError:
            self._parser.error('Failed to encode dataset.')
        except KeyboardInterrupt:
            self._parser.terminate('Encoding was canceled.')
