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

from collections import OrderedDict

# Package dependencies

from dtb.core.constants import DATA_DIR
from dtb.core.helpers import Number
from dtb.core.helpers.filesystem import Directory, File
from dtb.core.helpers.markup import GithubMarkdown as Markdown
from dtb.databases import DatabaseRepository
from dtb.databases.entities import Entities
from dtb.formats import FormatRepository

# Classes


class Readme(object):
    '''
    A README documentation file.
    '''

    def __init__(self, readmeFile, stubFile=None):
        '''
        Constructor.

        Arguments:
            readmeFile (dtb.core.helpers.filesystem.File): The README file
            stubFile (dtb.core.helpers.filesystem.File): The README stub file
        '''
        self._readmeFile = readmeFile
        self._stubFile = stubFile
        self._stub = self._stubFile.read() if stubFile else ''
        self._data = OrderedDict()

        # Load databases
        for base_year in DatabaseRepository.listYears():
            base_file = DATA_DIR / base_year / 'dtb.json'

            if base_file.exists():
                self._data[base_year] = json.load(File(base_file))

    def render(self):
        '''
        Renders the file.
        '''
        raise NotImplementedError

    def write(self):
        '''
        Writes the file to disk.
        '''
        self._readmeFile.write(self.render())


class ProjectReadme(Readme):
    '''
    The project README documentation file.
    '''

    def render(self):
        '''
        Renders the file.
        '''
        return self._stub.format(
            database_records=self.renderDatabaseRecords().strip(),
            database_formats=self.renderDatabaseFormats().strip()
        )

    def renderDatabaseRecords(self):
        '''
        Renders the available database records counts.
        '''
        headers = ['Base'] + [
            Markdown.code(entity.table) for entity in Entities
        ]
        alignment = ['>'] * 7
        data = [
            [Markdown.bold(base)] + [
                '{:,d}'.format(len(self._data[base][entity.table])) \
                    if entity.table in self._data[base] else '-'
                for entity in Entities
            ]
            for base in self._data
        ]

        return Markdown.table([headers] + data, alignment)

    def renderDatabaseFormats(self):
        '''
        Renders the available database formats.
        '''
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
    '''
    A database README documentation file.
    '''

    def __init__(self, base, readmeFile, stubFile):
        '''
        Constructor.

        Arguments:
            base (dtb.databases.Database): The database instance
            readmeFile (dtb.core.helpers.filesystem.File): The README file
            stubFile (dtb.core.helpers.filesystem.File): The README stub file
        '''
        super(self.__class__, self).__init__(readmeFile, stubFile)

        self._base = base
        self._baseDir = Directory(readmeFile.parent)

    def render(self):
        '''
        Renders the file.
        '''

        return self._stub.format(
            db_year=self._base.year,
            db_records=self.renderDatabaseRecords().strip(),
            db_files=self.renderDatabaseFiles().strip()
        )

    def renderDatabaseRecords(self):
        '''
        Renders the database records counts.
        '''
        headers = ['Table', 'Records']
        alignment = ['>', '>']
        data = [
            [Markdown.code(entity.table),
             '{:,d}'.format(len(self._data[self._base.year][entity.table]))]
            for entity in Entities
            if entity.table in self._data[self._base.year]
        ]

        return Markdown.table([headers] + data, alignment)

    def renderDatabaseFiles(self):
        '''
        Renders the database files.
        '''
        headers = ['File', 'Format', 'Size', 'Savings']
        alignment = ['<', '^', '>', '>']
        data = []

        for base_file in self._baseDir.files(pattern='dtb*'):
            raw_file = File(self._baseDir.parent / base_file.name)
            base_format = '-'

            if base_file.format:
                base_format = Markdown.link(base_file.format.info,
                                            base_file.format.friendlyName)

            base_info = [
                Markdown.code(base_file.name),
                base_format,
                '{:9,d}'.format(base_file.size),
            ]

            if raw_file.exists():
                savings = Number.percentDifference(base_file.size, raw_file.size)
                base_info.append('{:>6.1f}%'.format(savings))

            data.append(base_info)

        if 'minified' in self._baseDir:
            return Markdown.table([headers] + data, alignment)

        return Markdown.table([headers[:3]] + [row[:3] for row in data],
                              alignment[:3])
