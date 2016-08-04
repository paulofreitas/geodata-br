#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Microsoft Excel Spreadsheet file parser
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

from os import devnull

# External compatibility dependencies

from builtins import range

# External dependencies

import xlrd

# Package dependencies

from dtb.core.logging import Logger
from dtb.databases.entities import DatabaseRow
from dtb.formats.xls import XlsFormat
from dtb.parsers import Parser

# Module logging

logger = Logger.instance(__name__)

# Classes


class XlsParser(Parser):
    '''
    Microsoft Excel Spreadsheet file parser class.
    '''

    # Parser format
    _format = XlsFormat

    def __init__(self, base):
        '''
        Constructor.

        Arguments:
            base (dtb.databases.Database): The database instance to parse
        '''
        super(self.__class__, self).__init__(base)

        self._book = xlrd.open_workbook(file_contents=self._base.read(),
                                        encoding_override='utf-8',
                                        logfile=open(devnull, 'w'),
                                        on_demand=True)
        self._sheet = self._book.sheet_by_name(self._base.sheet)

    def parseColumns(self):
        '''
        Parses the database columns.
        '''
        logger.debug('Parsing database cols...')

        return DatabaseRow().columns[:self._sheet.ncols]

    def parseRows(self):
        '''
        Parses the database rows.
        '''
        logger.debug('Parsing database rows...')

        rows = []

        for row_id in range(self._sheet.nrows):
            # Skip headers
            if row_id == 0:
                continue

            row_data = [unicode(col) for col in self._sheet.row_values(row_id)]
            rows.append(self.parseRow(row_data))

        return rows

    def parseRow(self, row_data):
        '''
        Parses a given database row.

        Arguments:
            row_data (list): The database row data
        '''
        row = DatabaseRow()
        base = int(self._base.year)

        # 12 cols
        if base in [2003, 2005, 2006, 2007, 2008, 2009, 2013]:
            (row.state_id, row.state_name,
             row.mesoregion_id, row.mesoregion_name,
             row.microregion_id, row.microregion_name,
             row.municipality_id, row.municipality_name,
             row.district_id, row.district_name,
             row.subdistrict_id, row.subdistrict_name) = row_data
        # 8 cols
        elif base in [2010, 2011, 2012]:
            (row.state_id, row.state_name,
             row.mesoregion_id, row.mesoregion_name,
             row.microregion_id, row.microregion_name,
             row.municipality_id, row.municipality_name) = row_data
        # 15 cols
        elif base == 2014:
            (row.state_id, row.state_name,
             row.mesoregion_id, row.mesoregion_name,
             row.microregion_id, row.microregion_name) = row_data[:6]
            row.municipality_id, row.municipality_name = row_data[7:9]
            row.district_id, row.district_name = row_data[10:12]
            row.subdistrict_id, row.subdistrict_name = row_data[13:15]

        row.normalize()

        return row
