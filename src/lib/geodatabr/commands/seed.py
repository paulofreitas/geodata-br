#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Seed command module."""
# Imports

# Built-in dependencies

from argparse import Namespace

# Package dependencies

from geodatabr.commands import Command
from geodatabr.core.logging import logger
from geodatabr.dataset.base import Database
from geodatabr.dataset.schema import ENTITIES
from geodatabr.dataset.seeders import SeederFactory, NothingToSeedError

# Classes


class SeedCommand(Command):
    """A command class to seed the dataset with records."""

    @property
    def name(self) -> str:
        """Gets the command name."""
        return 'seed'

    @property
    def description(self) -> str:
        """Gets the command description."""
        return 'Seed the dataset with records'

    def handle(self, args: Namespace):
        """Handles the command."""
        try:
            Database.create()

            for entity in ENTITIES:
                logger().info('> Seeding table "%s"...', entity.__table__.name)

                try:
                    SeederFactory(entity).run()
                except NothingToSeedError:
                    logger().warning('Nothing to seed.')
        except KeyboardInterrupt:
            logger().warning('Seeding was canceled.')
