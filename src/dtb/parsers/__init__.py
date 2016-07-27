#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Database parsers package

This package provides the database parser modules.
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

from abc import ABCMeta as AbstractClass

# External compatibility dependencies

from future.utils import iteritems, itervalues, with_metaclass

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT License'

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
