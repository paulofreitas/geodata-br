#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Refresh command module."""
# Imports

# Built-in dependencies

from argparse import Namespace

# Package dependencies

from geodatabr.commands import Command
from geodatabr.commands.seed import SeedCommand
from geodatabr.core.logging import logger
from geodatabr.dataset.base import DatabaseHelper

# Classes


class RefreshCommand(Command):
    """A command class to reset and re-run all dataset seeders."""

    @property
    def name(self) -> str:
        """Gets the command name."""
        return 'refresh'

    @property
    def description(self) -> str:
        """Gets the command description."""
        return 'Reset and re-run all dataset seeders'

    def handle(self, args: Namespace):
        """Handles the command."""
        try:
            logger().info('> Clearing the dataset...')
            DatabaseHelper.clear()

            SeedCommand(self.application).handle(args)
        except KeyboardInterrupt:
            logger().warning('Refreshing was canceled.')
