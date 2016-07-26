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

from dtb.commands import CliParser
from dtb.core.entities import TerritorialBase
from dtb.core.helpers import ProjectReadme, DatabaseReadme, \
                             BASE_DIR, DATA_DIR, PKG_DIR

# Module metadata

__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT'
__version__ = '1.0-dev'
__usage__ = '%(prog)s'
__epilog__ = 'Report bugs and feature requests to {}.' \
    .format('https://github.com/paulofreitas/dtb-ibge/issues')

# Classes


class TerritorialDataDocBuilder(CliParser):
    '''Documentation builder command.'''

    def __init__(self):
        super(self.__class__, self).__init__(description=__doc__,
                                             usage=__usage__,
                                             epilog=__epilog__,
                                             version=__version__)

    def parse(self):
        '''Parses the given command line arguments.'''
        args = super(self.__class__, self).parse()

        ProjectReadme(path(BASE_DIR, 'README.md'),
                      path(PKG_DIR, 'data/stubs/README.stub.md')) \
            .write()

        for base in TerritorialBase.bases:
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
    TerritorialDataDocBuilder().parse()
