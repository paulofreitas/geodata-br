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
# -- Metadata -----------------------------------------------------------------

__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT'
__version__ = '1.0-dev'
__usage__ = '%(prog)s'
__epilog__ =\
    'Report bugs and feature requests to https://github.com/paulofreitas/dtb-ibge/issues.'

# -- Imports ------------------------------------------------------------------

# Built-in modules

import json

from os.path import basename, getsize as filesize, join as path, realpath

# Package modules

from dtb.core.entities import TerritorialBase, TerritorialData
from dtb.core.helpers import CliParser, Directory, File, Markdown, Number, \
                             String, BASE_DIR, DATA_DIR, PKG_DIR
from dtb.core.value_objects import Struct

# -- Classes ------------------------------------------------------------------


class Readme(object):
    data = Struct((base,
                   json.load(open(path(DATA_DIR, base, 'dtb.json'))))
                  for base in TerritorialBase.bases)

    def __init__(self, readme_file, stub_file=None):
        self._readme_file = realpath(readme_file)
        self._stub_file = realpath(stub_file) if stub_file else None
        self._readme = ''
        self._stub = ''

        with open(self._readme_file) as readme:
            self._readme = readme.read()

        if stub_file:
            with open(self._stub_file) as stub:
                self._stub = stub.read()

    def write(self):
        with open(self._readme_file, 'w') as readme:
            readme.write(self.render())


class ProjectReadme(Readme):
    def render(self):
        return self._stub.format(
            database_records=self.renderDatabaseRecords().strip(),
            database_formats=self.renderDatabaseFormats().strip()
        )

    def renderDatabaseRecords(self):
        headers = ['Base'] + [
            Markdown.code(table) for table in TerritorialData.tables
        ]
        alignment = ['>'] * 7
        data = [
            [Markdown.bold(base)] + [
                '{:,d}'.format(len(self.data[base][table])) \
                    if table in self.data[base] else '-'
                for table in TerritorialData.tables
            ]
            for base in TerritorialBase.bases
        ]

        return Markdown.table([headers] + data, alignment)

    def renderDatabaseFormats(self):
        formats = ', '.join(format for format in sorted(File.formats.values(),
                                                        key=lambda v: v.upper()))

        return String.rreplace(formats, ', ', ' and ', 1)


class DatabaseReadme(Readme):
    def __init__(self, readme_file, stub_file, base_dir):
        super(self.__class__, self).__init__(readme_file, stub_file)

        self.base_dir = realpath(base_dir)
        self.base = basename(base_dir)

    def render(self):
        return self._stub.format(
            db_year=self.base,
            db_records=self.renderDatabaseRecords().strip(),
            db_files=self.renderDatabaseFiles().strip()
        )

    def renderDatabaseRecords(self):
        headers = ['Table', 'Records']
        alignment = ['>', '>']
        data = [
            [Markdown.code(table),
             '{:,d}'.format(len(self.data[self.base][table]))]
             for table in TerritorialData.tables
             if table in self.data[self.base]
        ]

        return Markdown.table([headers] + data, alignment)

    def renderDatabaseFiles(self):
        headers = ['File', 'Format', 'Size', 'Savings']
        alignment = ['<', '^', '>', '>']
        data = [
            [Markdown.code(file.basename),
             file.format,
             '{:9,d}'.format(file.size),
             '{:>6.1f}%'.format(Number.percentDifference(file.size,
                 File(file.filename.replace('minified/', '')).size))]
            for file in Directory(self.base_dir).files(startswith='dtb')
        ]

        if 'minified' in self.base_dir:
            return Markdown.table([headers] + data, alignment)

        return Markdown.table([headers[:3]] + [row[:3] for row in data],
                              alignment[:3])


class TerritorialDataDocBuilder(CliParser):
    def __init__(self):
        super(self.__class__, self).__init__(description=__doc__,
                                             usage=__usage__,
                                             epilog=__epilog__,
                                             version=__version__)

    def parse(self):
        args = super(self.__class__, self).parse()

        ProjectReadme(path(BASE_DIR, 'README.md'),
                      path(PKG_DIR, 'docs/README.stub.md')) \
            .write()

        for base in TerritorialBase.bases:
            # Create raw database READMEs
            DatabaseReadme(path(DATA_DIR, base, 'README.md'),
                           path(PKG_DIR, 'docs/BASE_README.stub.md'),
                           path(DATA_DIR, base)) \
                .write()

            # Create minified database READMEs
            DatabaseReadme(path(DATA_DIR, 'minified', base, 'README.md'),
                           path(PKG_DIR, 'docs/BASE_README.stub.md'),
                           path(DATA_DIR, 'minified', base)) \
                .write()

if __name__ == '__main__':
    TerritorialDataDocBuilder().parse()
