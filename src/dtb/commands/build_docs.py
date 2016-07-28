#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Build documentation command module
'''
# Imports

# Built-in dependencies

from os.path import join as path

# Package dependencies

from dtb.commands import Command
from dtb.core.constants import BASE_DIR, DATA_DIR, PKG_DIR
from dtb.core.helpers.documentation import ProjectReadme, DatabaseReadme
from dtb.databases import Database

# Classes


class DocumentationBuilderCommand(Command):
    '''The documentation builder command.'''

    @property
    def usage(self):
        '''Defines the command usage syntax.'''
        return '%(prog)s'

    @property
    def description(self):
        '''Defines the command description.'''
        return __doc__

    @property
    def epilog(self):
        '''Defines the command epilog message.'''
        return 'Report bugs and feature requests to {}.' \
            .format('https://github.com/paulofreitas/dtb-ibge/issues')

    def run(self):
        '''Parses the given command line arguments.'''
        self.parse()

        ProjectReadme(path(BASE_DIR, 'README.md'),
                      path(PKG_DIR, 'data/stubs/README.stub.md')) \
            .write()

        for base in Database.bases:
            # Create raw database READMEs
            DatabaseReadme(path(DATA_DIR, base, 'README.md'),
                           path(PKG_DIR, 'data/stubs/BASE_README.stub.md'),
                           path(DATA_DIR, base)) \
                .write()

            # Create minified database READMEs
            DatabaseReadme(path(DATA_DIR, 'minified', base, 'README.md'),
                           path(PKG_DIR, 'data/stubs/BASE_README.stub.md'),
                           path(DATA_DIR, 'minified', base)) \
                .write()


if __name__ == '__main__':
    DocumentationBuilderCommand().run()
