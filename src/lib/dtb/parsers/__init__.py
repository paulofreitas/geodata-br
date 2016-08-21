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

# Built-in imports

from collections import OrderedDict

# External compatibility dependencies

from future.utils import itervalues

# Package dependencies

from dtb.core.logging import Logger
from dtb.core.types import AbstractClass, Map
from dtb.databases.entities import DatabaseData

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT License'

# Module logging

logger = Logger.instance(__name__)

# Classes


class Parser(AbstractClass):
    '''
    Abstract base parser class.
    '''

    # Parser format
    _format = None

    def __init__(self, base):
        '''
        Constructor.

        Arguments:
            base (dtb.databases.Database): A database instance to parse
        '''
        self._base = base
        self._columns = self._parseColumns(localized=False)
        self._names = OrderedDict()

    def __call__(self, **options):
        '''
        Allows parsing the database calling the parser instance.

        Arguments:
            options (dict): The parsing options

        Returns:
            dtb.databases.DatabaseData: The parsed database data

        Raises:
            ParseError: When a database fails to parse
        '''
        return self.parse()

    def parse(self, **options):
        '''
        Parses the database.

        Arguments:
            options (dict): The parsing options

        Returns:
            dtb.databases.DatabaseData: The parsed database data

        Raises:
            ParseError: When a database fails to parse
        '''
        try:
            logger.debug('Parsing database...')

            # Build database columns
            columns = self._parseColumns()

            # Build database rows
            rows = self._parseRows()

            # Build database records
            records = self._parseRecords(rows)

            logger.debug('Finished parsing database.')

            return DatabaseData(self._base, columns, rows, records)
        except:
            raise ParseError('Failed to parse data using the given parser')

    def _parseColumns(self, **options):
        '''
        Parses the database columns.

        Arguments:
            options (dict): The parsing options

        Returns:
            list: A list with parsed database columns
        '''
        raise NotImplementedError

    def _parseRows(self):
        '''
        Parses the database rows.

        Returns:
            list: A list with parsed database rows
        '''
        raise NotImplementedError

    def _parseRecords(self, rows):
        '''
        Parses the database records

        Returns:
            dict: The database records
        '''
        records = {}

        for entity in self._base.entities:
            entity_records = []
            last_entity = None

            for row in rows:
                current_entity = entity.make(row).data

                if (current_entity != last_entity
                        and None not in itervalues(current_entity)
                        and current_entity not in entity_records):
                    entity_records.append(current_entity)

                last_entity = current_entity

            records[entity.table] = sorted(entity_records,
                                           key=lambda row: row['id'])

        return records

    def _bindNames(self, row):
        '''
        Binds recorded names into given row.

        Arguments:
            row (dtb.databases.entities.DatabaseRow): The database row to bind
        '''
        columns = zip(*[reversed(self._columns)] * 2)
        column_names = [column_name for (column_name, column_id) in columns]

        for idx, (column_name, column_id) in enumerate(columns):
            value = row.__dict__[column_id]

            if value and int(value):
                self._names[column_name] = row._name

                for column in column_names[idx:]:
                    row.__dict__[column] = self._names[column]

                break


class ParserFactory(object):
    '''
    Parser factory class.
    '''

    @classmethod
    def fromFormat(cls, _format):
        '''
        Factories a parser class for a given format.

        Arguments:
            _format (str): The file format name to retrieve a parser

        Returns:
            Parser: The parser class instance

        Raises:
            UnknownParserError: When a given file format is not found
        '''
        for parser in Parser.childs():
            if parser._format().name == _format:
                return parser

        raise UnknownParserError('No parser found for format: {}' \
                                     .format(_format))


class ParseError(Exception):
    '''
    Generic exception class for parsing errors.
    '''
    pass


class UnknownParserError(ParseError):
    '''
    Exception class raised when a given parser is not found.
    '''
    pass
