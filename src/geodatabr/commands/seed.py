#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Seed command module."""
# Imports

# Built-in dependencies

import argparse

# Package dependencies

from geodatabr.core import commands, datasets, logging
from geodatabr.dataset import schema, seeders

# Classes


class SeedCommand(commands.Command):
    """A command class to seed datasets with records."""

    @property
    def name(self) -> str:
        """Gets the command name."""
        return 'seed'

    @property
    def description(self) -> str:
        """Gets the command description."""
        return 'Seed datasets with records'

    def handle(self, args: argparse.Namespace):
        """
        Handles the command.

        Args:
            args: The command arguments
        """
        try:
            logger = logging.logger()
            datasets.Database.create()

            for entity in schema.ENTITIES:
                logger.info('> Seeding dataset "%s"...', entity.__table__.name)

                try:
                    seeders.SeederFactory.fromEntity(entity).run()
                except seeders.NothingToSeedError:
                    logger.warning('Nothing to seed.')
        except KeyboardInterrupt:
            self._parser.terminate('Seeding was canceled.')
