#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Generic Data File file parser module
'''
# Imports

# Package dependencies

from places.core.logging import Logger
from places.core.types import Bytes
from places.databases.entities import DatabaseRow
from places.formats.dat import DatFormat
from places.parsers import Parser

# Module logging

logger = Logger.instance(__name__)

# Classes


class DatParser(Parser):
    '''
    Generic Data File file parser class.
    '''

    # Parser format
    _format = DatFormat

    def __init__(self, base):
        '''
        Constructor.

        Arguments:
            base (places.databases.Database): The database instance to parse
        '''
        super().__init__(base)

        self._rows = self._base.read().splitlines()

    def _parseColumns(self, **options):
        '''
        Parses the database columns.

        Arguments:
            options (dict): The parsing options

        Returns:
            list: A list with parsed database columns
        '''
        return DatabaseRow().columns(options.get('localized', True))

    def _parseRows(self):
        '''
        Parses the database rows.

        Returns:
            list: A list with parsed database rows
        '''
        rows = []

        for row_data in self._rows:
            # Stop at EOF
            if row_data == '\x1a':
                break

            rows.append(self._parseRow(Bytes(row_data)))

        return rows

    def _parseRow(self, row_data):
        '''
        Parses a given database row.

        Arguments:
            row_data (bytes): The database row data

        Returns:
            places.databases.entities.DatabaseRow: The parsed database row
        '''
        row = DatabaseRow()

        row.state_id, row.mesoregion_id, row.microregion_id, \
        row.municipality_id, row.district_id, row.subdistrict_id, \
        name = row_data.unpack('2s2s3s5s2s2s')
        row._name = name.replace('\x8c', '\x55')

        self._bindNames(row)

        return row.normalize()
