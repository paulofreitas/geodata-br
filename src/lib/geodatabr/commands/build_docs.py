#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Build documentation command module
'''
# Imports

# Package dependencies

from geodatabr.commands import Command
from geodatabr.core.constants import DATA_DIR
from geodatabr.core.helpers.documentation import ProjectReadme, DatasetReadme
from geodatabr.core.helpers.filesystem import File
from geodatabr.core.i18n import Translator
from geodatabr.core.logging import Logger
from geodatabr.databases import DatabaseRepository

# Module logging

logger = Logger.instance(__name__)

# Classes


class DocumentationBuilderCommand(Command):
    '''
    The documentation builder command.
    '''

    @property
    def name(self):
        '''
        Defines the command name.
        '''
        return 'build:docs'

    @property
    def description(self):
        '''
        Defines the command description.
        '''
        return 'Builds the documentation'

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
        logger.info('Generating project README...')

        ProjectReadme().write()

        for locale in Translator.locales():
            logger.info('Generating "{}" language dataset READMEs...'.format(locale))

            for dataset in DatabaseRepository.findAll():
                dataset_dir = DATA_DIR / locale / dataset.year

                if dataset_dir.exists():
                    # Create dataset README
                    DatasetReadme(dataset, dataset_dir, locale).write()
