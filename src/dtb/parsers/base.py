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
from __future__ import absolute_import

# Imports

# Built-in dependencies

from abc import ABCMeta as AbstractClass

# External compatibility dependencies

from future.utils import iteritems, itervalues, with_metaclass

# Classes


class Parser(object, with_metaclass(AbstractClass)):
    '''Abstract base parser class.'''

    # Parser format
    _format = None

    def __init__(self, base, logger):
        '''Constructor.

        :param base: a territorial base instance to parse
        :param logger: a logger instance to log
        '''
        self._logger = logger
        self._base = base
        self._data = base._data

    def initialize(self):
        '''Initialize the internal data columns.'''
        for entity in self._data.entities:
            self._data._cols.append('id_' + entity.table)
            self._data._cols.append('nome_' + entity.table)

    def parse(self):
        '''Parses the database.'''
        self._logger.debug('Parsing database...')

        cols = self.parseColumns()
        rows = self.parseRows()

        self.initialize()

        # Build database columns
        self._data._cols = cols

        # Build database rows
        self._data._rows.extend(row.value for row in rows)

        # Build database records
        for entity in self._data.entities:
            records = []

            for row in rows:
                row_data = getattr(row, entity.table)

                if None not in itervalues(row_data) \
                        and row_data not in records:
                    records.append(row_data)

            self._data._dict[entity.table] = sorted(records,
                                                    key=lambda row: row.id)

        return self._data

    def parseColumns(self):
        '''Parses the database columns.'''
        raise NotImplementedError

    def parseRows(self):
        '''Parsers the database rows.'''
        raise NotImplementedError


class ParserFactory(object):
    '''Parser factory class.'''

    @classmethod
    def fromFormat(cls, _format):
        '''Factories a parser class for a given format.

        :param _format: the file format name to retrieve a parser'''
        parsers = {parser._format().name: parser
                   for parser in Parser.__subclasses__()}

        try:
            return parsers[_format]
        except KeyError:
            raise UnknownParserError('No parser found for format: {}' \
                                         .format(_format))


class ParserError(Exception):
    '''Generic exception class for parsing errors.'''
    pass


class UnknownParserError(ParserError):
    '''Exception class raised when a given parser is not found.'''
    pass
