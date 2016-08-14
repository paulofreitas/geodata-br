#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Generic Data File file parser module
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

from collections import OrderedDict

# Package dependencies

from dtb.core.logging import Logger
from dtb.core.types import Bytes
from dtb.databases.entities import DatabaseRow
from dtb.formats.dat import DatFormat
from dtb.parsers import Parser

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
            base (dtb.databases.Database): The database instance to parse
        '''
        super(self.__class__, self).__init__(base)

        self._rows = self._base.read().splitlines()
        self._names = OrderedDict()

    def _parseColumns(self):
        '''
        Parses the database columns.

        Returns:
            list: A list with parsed database columns
        '''
        logger.debug('Parsing database cols...')

        return DatabaseRow().columns

    def _parseRows(self):
        '''
        Parses the database rows.

        Returns:
            list: A list with parsed database rows
        '''
        logger.debug('Parsing database rows...')

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
            dtb.databases.entities.DatabaseRow: The parsed database row
        '''
        row = DatabaseRow()

        row.state_id, row.mesoregion_id, row.microregion_id, \
        row.municipality_id, row.district_id, row.subdistrict_id, \
        name = row_data.unpack('2s2s3s5s2s2s')

        columns = zip(*[reversed(row.columns)] * 2)
        column_names = [column_name for (column_name, column_id) in columns]

        for idx, (column_name, column_id) in enumerate(columns):
            if int(getattr(row, column_id)):
                self._names[column_name] = name.replace('\x8c', '\x55')

                for column in column_names[idx:]:
                    setattr(row, column, self._names[column])

                break

        return row.normalize()
