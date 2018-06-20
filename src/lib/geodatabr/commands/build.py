#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Build command module."""
# Imports

# Built-in dependencies

from argparse import Namespace

# Package dependencies

from geodatabr.core.commands import Command
from geodatabr.core.encoders import EncoderFactory, EncoderFormatRepository, \
    EncodeError
from geodatabr.core.helpers.documentation import ProjectReadme, DatasetReadme
from geodatabr.core.helpers.filesystem import Directory, Path
from geodatabr.core.i18n import Translator
from geodatabr.core.logging import logger

# Classes


class BuildCommand(Command):
    """A command class to build the dataset files."""

    @property
    def name(self) -> str:
        """Gets the command name."""
        return 'build'

    @property
    def description(self) -> str:
        """Gets the command description."""
        return 'Build the dataset files'

    @property
    def usage(self) -> str:
        """Gets the command usage syntax."""
        return '%(prog)s [-l LOCALE] [-f FORMAT]'

    def configure(self):
        """Defines the command arguments."""
        locales = Translator.locales()
        formats = EncoderFormatRepository.listNames()

        self.addArgument('-l', '--locales',
                         metavar='LOCALE',
                         nargs='*',
                         choices=locales,
                         default=locales,
                         help=('Locales to build the dataset.\n'
                               'Options: %(choices)s\n'
                               'Defaults to all available.'))
        self.addArgument('-f', '--formats',
                         metavar='FORMAT',
                         nargs='*',
                         choices=formats,
                         default=formats,
                         help=('File formats to build the dataset.\n'
                               'Options: %(choices)s\n'
                               'Defaults to all available.'))

    def handle(self, args: Namespace):
        """Handles the command."""
        try:
            for locale in args.locales:
                Translator.locale = locale

                logger().info('> Building locale: %s', locale)

                dataset_dir = Directory(Path.DATA_DIR / locale)
                dataset_dir.create(parents=True)

                with dataset_dir:
                    for dataset_format in args.formats:
                        encoder = EncoderFactory.fromFormat(dataset_format)

                        logger().info('Encoding dataset to %s format...',
                                      encoder.format().friendlyName)

                        serializer = encoder.serializer(
                            **encoder.serializationOptions)

                        encoder.encodeToFile(serializer.serialize())

                    logger().info('Generating dataset README file...')

                    DatasetReadme(dataset_dir).write()

            logger().info('Generating project README file...')

            ProjectReadme().write()
        except EncodeError:
            logger().error('Failed to encode dataset.')
        except KeyboardInterrupt:
            logger().info('Building was canceled.')
