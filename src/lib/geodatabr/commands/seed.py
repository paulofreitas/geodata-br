#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Seed command module
'''
# Imports

# Package dependencies

from geodatabr.commands import Command
from geodatabr.core.logging import logger
from geodatabr.dataset.base import DatabaseHelper
from geodatabr.dataset.schema import Entities
from geodatabr.dataset.seeders import SeederFactory, NothingToSeedError

# Classes


class SeedCommand(Command):
    '''
    A command class to seed the dataset with records.
    '''

    @property
    def name(self):
        '''
        Defines the command name.
        '''
        return 'seed'

    @property
    def description(self):
        '''
        Defines the command description.
        '''
        return 'Seed the dataset with records'

    @property
    def usage(self):
        '''
        Defines the command usage syntax.
        '''
        return '%(prog)s'

    def handle(self, args):
        '''
        Handles the command.
        '''
        try:
            DatabaseHelper.create()

            for entity in Entities:
                logger().info('> Seeding table "%s"...', entity.__table__.name)

                try:
                    SeederFactory(entity).run()
                except NothingToSeedError:
                    logger().warning('Nothing to seed.')
        except KeyboardInterrupt:
            logger().warning('Seeding was canceled.')
