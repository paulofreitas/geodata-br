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

# Package dependencies

from dtb.core.constants import DATA_DIR
from dtb.core.helpers import Number
from dtb.core.helpers.filesystem import Directory, File
from dtb.core.helpers.markup import Markdown
from dtb.core.types import Struct
from dtb.databases import DatabaseRepository
from dtb.databases.entities import DatabaseData
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
        self._contents = self._readmeFile.read()
        self._stub = self._stubFile.read() if stubFile else ''
        self._data = Struct()

        # Load databases
        for base in DatabaseRepository.listYears():
            self._data[base] = json.load(File(DATA_DIR / base / 'dtb.json'))

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
            Markdown.code(entity.table) for entity in DatabaseData.entities
        ]
        alignment = ['>'] * 7
        data = [
            [Markdown.bold(base)] + [
                '{:,d}'.format(len(self._data[base][entity.table])) \
                    if entity.table in self._data[base] else '-'
                for entity in DatabaseData.entities
            ]
            for base in DatabaseRepository.listYears()
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

    def __init__(self, readmeFile, stubFile):
        '''
        Constructor.

        Arguments:
            readmeFile (dtb.core.helpers.filesystem.File): The README file
            stubFile (dtb.core.helpers.filesystem.File): The README stub file
        '''
        super(self.__class__, self).__init__(readmeFile, stubFile)

        self._baseDir = Directory(readmeFile.parent)
        self._base = self._baseDir.name

    def render(self):
        '''
        Renders the file.
        '''

        return self._stub.format(
            db_year=self._base,
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
             '{:,d}'.format(len(self._data[self._base][entity.table]))]
            for entity in DatabaseData.entities
            if entity.table in self._data[self._base]
        ]

        return Markdown.table([headers] + data, alignment)

    def renderDatabaseFiles(self):
        '''
        Renders the database files.
        '''
        headers = ['File', 'Format', 'Size', 'Savings']
        alignment = ['<', '^', '>', '>']
        data = []

        for baseFile in self._baseDir.files(pattern='dtb*'):
            baseFormat = '-'

            if baseFile.format:
                baseFormat = Markdown.link(baseFile.format.info,
                                           baseFile.format.friendlyName)

            data.append([
                Markdown.code(baseFile.name),
                baseFormat,
                '{:9,d}'.format(baseFile.size),
                '{:>6.1f}%'.format(Number.percentDifference(baseFile.size,
                    File(str(baseFile).replace('minified/', '')).size))
            ])

        if 'minified' in self._baseDir:
            return Markdown.table([headers] + data, alignment)

        return Markdown.table([headers[:3]] + [row[:3] for row in data],
                              alignment[:3])
