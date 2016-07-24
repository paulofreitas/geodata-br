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
from os import listdir
from os.path import abspath, basename, dirname, getsize as filesize, \
                    join as path, realpath, splitext

# Package dependencies

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


class String(object):
    @staticmethod
    def rreplace(string, old, new, occurrence):
        return new.join(string.rsplit(old, occurrence))


class Directory(object):
    def __init__(self, dirname):
        self._dirname = dirname

    @property
    def basename(self):
        return basename(self._dirname)

    def files(self, startswith=''):
        return [File(realpath(path(self._dirname, filename)))
                for filename in listdir(realpath(self._dirname))
                if filename.startswith(startswith)]


class File(object):
    formats = {
        '.csv': 'CSV',
        '.fdb': 'Firebird',
        '.json': 'JSON',
        '.phpd': 'Serialized PHP',
        '.plist': 'p-list',
        '.sql': 'SQL',
        '.sqlite3': 'SQLite 3',
        '.xml': 'XML',
        '.yaml': 'YAML'
    }

    def __init__(self, filename):
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    @property
    def basename(self):
        return basename(self._filename)

    @property
    def extension(self):
        return splitext(self._filename)[1]

    @property
    def format(self):
        return self.formats.get(self.extension, '-')

    @property
    def size(self):
        return filesize(self._filename)


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
                         for index, item in enumerate(items))

    @staticmethod
    def unorderedList(items, bullet_char='*'):
        '''Generates a bullet list.'''
        assert bullet_char in ['*', '-', '+'], 'Invalid bullet char'

        return '\n'.join('{} {}'.format(bullet_char, item) for item in items)

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
        assert depth >=1 and depth <= 6, 'Invalid depth'

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
        return self._stub.format(
            database_records=self.renderDatabaseRecords().strip(),
            database_formats=self.renderDatabaseFormats().strip()
        )

    def renderDatabaseRecords(self):
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
        headers = ['File', 'Format', 'Size', 'Savings']
        alignment = ['<', '^', '>', '>']
        data = [
            [Markdown.code(base_file.basename),
             base_file.format,
             '{:9,d}'.format(base_file.size),
             '{:>6.1f}%'.format(Number.percentDifference(base_file.size,
                 File(base_file.filename.replace('minified/', '')).size))]
            for base_file in Directory(self.base_dir).files(startswith='dtb')
        ]

        if 'minified' in self.base_dir:
            return Markdown.table([headers] + data, alignment)

        return Markdown.table([headers[:3]] + [row[:3] for row in data],
                              alignment[:3])
