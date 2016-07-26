#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Brazilian territorial distribution data exporter

The MIT License (MIT)

Copyright (c) 2013-2016 Paulo Freitas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
# Imports

# Built-in dependencies

from os.path import join as path

# Package dependencies

from dtb.cli.base import CliParser
from dtb.core.entities import TerritorialBase
from dtb.core.helpers import ProjectReadme, DatabaseReadme, \
                             BASE_DIR, DATA_DIR, PKG_DIR

# Metadata

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
