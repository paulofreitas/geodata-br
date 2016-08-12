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
from dtb.core.constants import BASE_DIR, DATA_DIR, SRC_DIR
from dtb.core.helpers.documentation import ProjectReadme, DatabaseReadme
from dtb.core.helpers.filesystem import File
from dtb.databases import DatabaseRepository

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
        ProjectReadme(File(BASE_DIR / 'README.md'),
                      File(SRC_DIR / 'data/stubs/README.stub.md')) \
            .write()

        base_readme_stub = File(SRC_DIR / 'data/stubs/BASE_README.stub.md')

        for base in DatabaseRepository.findAll():
            base_dir = DATA_DIR / base.year
            min_base_dir = base_dir / 'minified'

            if base_dir.exists():
                # Create raw database READMEs
                DatabaseReadme(base,
                               File(base_dir / 'README.md'),
                               base_readme_stub) \
                    .write()

            if min_base_dir.exists():
                # Create minified database READMEs
                DatabaseReadme(base,
                               File(min_base_dir / 'README.md'),
                               base_readme_stub) \
                    .write()
