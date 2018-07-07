#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Refresh command module."""
# Imports

# Built-in dependencies

import argparse

# Package dependencies

from geodatabr.commands import seed
from geodatabr.core import commands, datasets, logging

# Classes


class RefreshCommand(commands.Command):
    """A command class to reset and re-run all datasets seeders."""

    @property
    def name(self) -> str:
        """Gets the command name."""
        return 'refresh'

    @property
    def description(self) -> str:
        """Gets the command description."""
        return 'Reset and re-run all datasets seeders'

    def handle(self, args: argparse.Namespace):
        """
        Handles the command.

        Args:
            args: The command arguments
        """
        try:
            logger = logging.logger()

            logger.info('> Clearing datasets...')
            datasets.Database.clear()

            seed.SeedCommand(self.application).handle(args)
        except KeyboardInterrupt:
            self._parser.terminate('Refreshing was canceled.')
