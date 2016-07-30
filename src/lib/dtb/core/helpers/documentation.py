#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Documentation helper module

This module provides helper classes to write documentation files.
'''
# Imports

# Built-in dependencies

import json

from os.path import basename, join as path, realpath

# Package dependencies

from dtb.core.constants import DATA_DIR
from dtb.core.entities import TerritorialData
from dtb.core.helpers import Number
from dtb.core.helpers.filesystem import Directory, File
from dtb.core.helpers.markup import Markdown
from dtb.core.value_objects import Struct
from dtb.databases import Database
from dtb.formats import FormatRepository

# Classes


class Readme(object):
    def __init__(self, readme_file, stub_file=None):
        self._readme_file = realpath(readme_file)
        self._stub_file = realpath(stub_file) if stub_file else None
        self._readme = ''
        self._stub = ''
        self._data = Struct((base,
                             json.load(open(path(DATA_DIR, base, 'dtb.json'))))
                            for base in Database.bases)

        with open(self._readme_file) as readme:
            self._readme = readme.read()

        if stub_file:
            with open(self._stub_file) as stub:
                self._stub = stub.read()

    def render(self):
        raise NotImplementedError

    def write(self):
        with open(self._readme_file, 'w') as readme:
            readme.write(self.render())


class ProjectReadme(Readme):
    def render(self):
        '''Renders the project README file.'''
        return self._stub.format(
            database_records=self.renderDatabaseRecords().strip(),
            database_formats=self.renderDatabaseFormats().strip()
        )

    def renderDatabaseRecords(self):
        '''Renders the available database records counts.'''
        headers = ['Base'] + [
            Markdown.code(entity.table) for entity in TerritorialData.entities
        ]
        alignment = ['>'] * 7
        data = [
            [Markdown.bold(base)] + [
                '{:,d}'.format(len(self._data[base][entity.table])) \
                    if entity.table in self._data[base] else '-'
                for entity in TerritorialData.entities
            ]
            for base in Database.bases
        ]

        return Markdown.table([headers] + data, alignment)

    def renderDatabaseFormats(self):
        '''Renders the available database formats.'''
        grouped_formats = FormatRepository.groupExportableFormatsByType()
        markdown = ''

        for format_type, formats in grouped_formats:
            markdown += '\n'.join([
                Markdown.header(format_type, depth=4),
                Markdown.unorderedList([
                    Markdown.link(_format.info, _format.friendlyName)
                    for _format in formats
                ]) + '\n'
            ])

        return markdown

class DatabaseReadme(Readme):
    def __init__(self, readme_file, stub_file, base_dir):
        '''Constructor.'''
        super(self.__class__, self).__init__(readme_file, stub_file)

        self.base_dir = realpath(base_dir)
        self.base = basename(base_dir)

    def render(self):
        '''Renders a database README file.'''

        return self._stub.format(
            db_year=self.base,
            db_records=self.renderDatabaseRecords().strip(),
            db_files=self.renderDatabaseFiles().strip()
        )

    def renderDatabaseRecords(self):
        '''Renders the database records counts.'''
        headers = ['Table', 'Records']
        alignment = ['>', '>']
        data = [
            [Markdown.code(entity.table),
             '{:,d}'.format(len(self._data[self.base][entity.table]))]
            for entity in TerritorialData.entities
            if entity.table in self._data[self.base]
        ]

        return Markdown.table([headers] + data, alignment)

    def renderDatabaseFiles(self):
        '''Renders the database files.'''
        headers = ['File', 'Format', 'Size', 'Savings']
        alignment = ['<', '^', '>', '>']
        data = []

        for base_file in Directory(self.base_dir).files(pattern='dtb*'):
            base_format = '-'

            if base_file.format:
                base_format = Markdown.link(base_file.format.info,
                                            base_file.format.friendlyName)

            data.append([
                Markdown.code(base_file.name),
                base_format,
                '{:9,d}'.format(base_file.size),
                '{:>6.1f}%'.format(Number.percentDifference(base_file.size,
                    File(str(base_file).replace('minified/', '')).size))
            ])

        if 'minified' in self.base_dir:
            return Markdown.table([headers] + data, alignment)

        return Markdown.table([headers[:3]] + [row[:3] for row in data],
                              alignment[:3])
