#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Brazilian territorial distribution data

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

import json

from collections import defaultdict
from os.path import abspath, basename, dirname, join as path, realpath
from pathlib import Path

# Package dependencies

from ..formats.base import FormatRepository, FormatError
from .value_objects import Struct

# Constants

PKG_DIR = abspath(path(dirname(__file__), '..'))
SRC_DIR = abspath(path(PKG_DIR, '..'))
BASE_DIR = abspath(path(SRC_DIR, '..'))
DATA_DIR = path(BASE_DIR, 'data')

# Classes


class Number(object):
    @staticmethod
    def percentDifference(from_value, to_value):
        return (1 - float(from_value) / float(to_value)) * 100


class Directory(object):
    def __init__(self, dirname):
        '''Constructor.

        :param dirname: the directory path to give a new Directory object
        '''
        self._path = Path(dirname)

    @property
    def name(self):
        '''Returns the directory name.'''
        return self._path.name

    def files(self, pattern='*'):
        '''Returns a list with all directory files matching the given pattern.'''
        return [File(_file) for _file in self._path.iterdir()
                if _file.match(pattern)]

    def __str__(self):
        '''String representation of this directory object.'''
        return str(self._path)


class File(object):
    def __init__(self, filename):
        '''Constructor.

        :param filename: the file path to give a new File object
        '''
        self._path = Path(filename)

    @property
    def name(self):
        '''Returns the file name.'''
        return self._path.name

    @property
    def path(self):
        '''Returns the file path.'''
        return self._path.parent

    @property
    def extension(self):
        '''Returns the file extension.'''
        return ''.join(self._path.suffixes)

    @property
    def format(self):
        '''Returns the file format.'''
        try:
            return FormatRepository.findFormatByExtension(self.extension)
        except FormatError:
            return None

    @property
    def size(self):
        '''Returns the file size.'''
        return self._path.stat().st_size


    def __str__(self):
        '''String representation of this file object.'''
        return str(self._path)


# Markdown generator
class Markdown(object):
    # Emphasis

    @staticmethod
    def bold(text, alternative=False):
        '''Creates a bold text.'''
        if alternative:
            return '__{}__'.format(text)

        return '**{}**'.format(text)

    @staticmethod
    def italic(text, alternative=True):
        '''Creates text in italics.'''
        if alternative:
            return '_{}_'.format(text)

        return '*{}*'.format(text)

    @staticmethod
    def strikethrough(text):
        '''Strikes through the provided text.'''
        return '~~{}~~'.format(text)

    # Lists

    @staticmethod
    def orderedList(items):
        '''Generates a numbered list.'''
        return '\n'.join('{}. {}'.format(index + 1, item)
                         for index, item in enumerate(items)) + '\n'

    @staticmethod
    def unorderedList(items, bullet_char='*'):
        '''Generates a bullet list.'''
        assert bullet_char in ['*', '-', '+'], 'Invalid bullet char'

        return '\n'.join('{} {}'.format(bullet_char, item)
                         for item in items) + '\n'

    # Others

    @staticmethod
    def blockquote(text, simple=False):
        '''Creates a block quoted text.'''
        if simple:
            return '> {}\n'.format(text)

        return '\n'.join(['> {}'.format(line) for line in text.splitlines()])

    @staticmethod
    def code(content, inline=True, syntax=None):
        if inline and not syntax:
            return '`{}`'.format(content)

        return '```{}\n{}\n```'.format(syntax or '', content)

    @staticmethod
    def header(heading_text, depth=1, alternative=False):
        '''Creates a header.'''
        assert depth >= 1 and depth <= 6, 'Invalid depth'

        if alternative and depth in (1, 2):
            return '\n'.join([
                heading_text,
                ['=', '-'][depth -1] * len(heading_text)
            ]) + '\n'

        return '#' * depth + ' ' + heading_text + '\n'

    @staticmethod
    def horizontalRule(rule_char='-'):
        '''Creates an horizontal rule.'''
        assert rule_char in ['-', '*', '_']

        return rule_char * 3 + '\n'

    @staticmethod
    def link(url, text='', title=''):
        '''Generates a link to an URL.'''
        if not text and not title:
            return url

        if not title:
            return '[{}]({})'.format(text, url)

        return '[{}]({} "{}")'.format(text, url, title)

    @staticmethod
    def literal(text):
        chars = '\\`*_{}[]()#+-.!'

        return ''.join('\\' + char if char in chars else char for char in text)

    @staticmethod
    def table(data, aligning=None):
        '''Generates a table from a 2 dimentional list.'''
        md = ''

        # No aligning: default is left
        if not aligning:
            aligning = ['<'] * len(data[0])

        if len(data[0]) > len(aligning):
            difference = len(data[0]) - len(aligning)
            aligning.extend(['<'] * difference)

        assert len(aligning) >= len(data[0])

        # Calculate max size of each column
        column_sizes = defaultdict(int)

        for row in data:
            for column, cell in enumerate(map(str, row)):
                column_sizes[column] = max(column_sizes[column], len(cell))

        # Headers

        md = '|{}|\n'.format('|'.join([
            (' {{:' + aligning[col] + '{}}} ').format(column_sizes[col])
                                              .replace('^', '<')
                                              .format(cell)
            for col, cell in enumerate(data[0])
        ]))

        # Heading separator
        md += '|{}|\n'.format('|'.join([
            ''.join([
                ':' if aligning[col] == '^' else ' ', # left char
                '-' * column_sizes[col],
                ' ' if aligning[col] == '<' else ':', # right char
            ])
            for col in range(len(data[0]))
        ]))

        # Data
        md += ''.join([
            '|{}|\n'.format('|'.join([
                (' {{:' + aligning[col] + '{}}} ').format(column_sizes[col])
                                                  .replace('^', '<')
                                                  .format(cell)
                for col, cell in enumerate(row)
            ]))
            for row in data[1:]
        ])

        return md


class Readme(object):
    def __init__(self, readme_file, stub_file=None):
        from .entities import TerritorialBase

        self._readme_file = realpath(readme_file)
        self._stub_file = realpath(stub_file) if stub_file else None
        self._readme = ''
        self._stub = ''
        self._data = Struct((base,
                             json.load(open(path(DATA_DIR, base, 'dtb.json'))))
                            for base in TerritorialBase.bases)

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
        from .entities import TerritorialBase, TerritorialData

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
            for base in TerritorialBase.bases
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
        from .entities import TerritorialData

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
