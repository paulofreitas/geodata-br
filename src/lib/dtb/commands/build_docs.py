#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Build documentation command module
'''
# Imports

# Package dependencies

from dtb.commands import Command
from dtb.core.constants import DATA_DIR
from dtb.core.helpers.documentation import ProjectReadme, DatasetReadme
from dtb.core.helpers.filesystem import File
from dtb.core.logging import Logger
from dtb.databases import DatabaseRepository

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

        for language_dir in DATA_DIR.directories():
            language = language_dir.name

            logger.info('Generating "{}" dataset READMEs...'.format(language))

            for dataset in DatabaseRepository.findAll():
                dataset_dir = language_dir / dataset.year
                min_dataset_dir = dataset_dir / 'minified'

                if dataset_dir.exists():
                    # Create raw dataset READMEs
                    DatasetReadme(dataset, dataset_dir, language).write()

                if min_dataset_dir.exists():
                    # Create minified dataset READMEs
                    DatasetReadme(dataset, min_dataset_dir, language).write()
