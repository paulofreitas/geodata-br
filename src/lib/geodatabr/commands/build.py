#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Build command module."""
# Imports

# Built-in dependencies

import argparse

# Package dependencies

from geodatabr.commands import encode
from geodatabr.core import commands, encoders, i18n, logging
from geodatabr.core.utils import documentation, io

# Classes


class BuildCommand(commands.Command):
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
        locales = i18n.Translator.locales()
        formats = encoders.EncoderFormatRepository.listNames()

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

    def handle(self, args: argparse.Namespace):
        """
        Handles the command.

        Args:
            args: The command arguments
        """
        try:
            encoder = encode.EncodeCommand(self.application)
            logger = logging.logger()

            for locale in args.locales:
                i18n.Translator.locale = locale

                logger.info('> Building locale: %s', locale)

                dataset_dir = io.Directory(io.Path.DATA_DIR / locale)
                dataset_dir.create(parents=True)

                with dataset_dir:
                    for dataset_format in args.formats:
                        encoder.configure()
                        encoder.handle(encoder.parse([
                            '--format', dataset_format,
                            '--locale', locale]))

                    logger.info('Generating dataset README file...')

                    documentation.DatasetReadme(dataset_dir).write()

            logger.info('Generating project README file...')

            documentation.ProjectReadme().write()
        except encoders.EncodeError:
            self._parser.error('Failed to build dataset.')
        except KeyboardInterrupt:
            self._parser.terminate('Building was canceled.')
