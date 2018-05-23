#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
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

from places.core.logging import Logger
from places.databases.entities import DatabaseRow
from places.formats.xls import XlsFormat
from places.parsers import Parser

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
            base (places.databases.Database): The database instance to parse
        '''
        super(self.__class__, self).__init__(base)

        self._book = xlrd.open_workbook(file_contents=self._base.read(),
                                        encoding_override='utf-8',
                                        logfile=open(devnull, 'w'),
                                        on_demand=True)
        self._sheet = self._book.sheet_by_name(self._base.sheet)
        self._lastrow = None

    def _parseColumns(self, **options):
        '''
        Parses the database columns.

        Arguments:
            options (dict): The parsing options

        Returns:
            list: A list with parsed database columns
        '''
        columns = DatabaseRow().columns(options.get('localized', True))
        base_year = int(self._base.year)

        if base_year in (1940, 1950, 1960, 1970, 1980):
            return columns[:2] + columns[6:8]
        elif base_year in (2010, 2011, 2012):
            return columns[:8]

        return columns

    def _parseRows(self):
        '''
        Parses the database rows.

        Returns:
            list: A list with parsed database rows
        '''
        rows = []

        for row_id in range(self._sheet.nrows):
            # Skip headers
            if row_id == 0:
                continue

            row_data = [col or None for col in self._sheet.row_values(row_id)]

            # Break on incomplete rows
            if len([col for col in row_data if col]) <= 1:
                break

            rows.append(self._parseRow(row_data))

        return rows

    def _parseRow(self, row_data):
        '''
        Parses a given database row.

        Arguments:
            row_data (list): The database row data

        Returns:
            places.databases.entities.DatabaseRow: The parsed database row
        '''
        row = DatabaseRow()
        normalization_options = {}
        base_year = int(self._base.year)

        if base_year in (1940, 1950, 1960, 1970, 1980):
            (row.state_id, row.state_name) = row_data[:2]
            (row.municipality_id, row.municipality_name) = row_data[3:5]
        elif base_year in (2000, 2004):
            if base_year == 2000:
                row.state_id, row.mesoregion_id, row.microregion_id, \
                row.municipality_id, row.district_id, row.subdistrict_id, \
                row._name = row_data[2:]
                normalization_options = dict(force_str=True)
            elif base_year == 2004:
                level, row.state_id, _id, row.district_id, \
                row.subdistrict_id, row._name = row_data
                level = int(level)

                if level in (5, 6, 7):
                    row.municipality_id = _id
                    row.microregion_id = str(self._lastrow.microregion_id)
                    row.mesoregion_id = str(self._lastrow.mesoregion_id)
                elif level == 8:
                    row.mesoregion_id = _id[:2]
                elif level == 9:
                    row.microregion_id = _id[:3]
                    row.mesoregion_id = str(self._lastrow.mesoregion_id)

                self._lastrow = row

            self._bindNames(row)
        elif base_year in (2003, 2005, 2006, 2007, 2008, 2009, 2013):
            (row.state_id, row.state_name,
             row.mesoregion_id, row.mesoregion_name,
             row.microregion_id, row.microregion_name,
             row.municipality_id, row.municipality_name,
             row.district_id, row.district_name,
             row.subdistrict_id, row.subdistrict_name) = row_data
        elif base_year in (2010, 2011, 2012):
            (row.state_id, row.state_name,
             row.mesoregion_id, row.mesoregion_name,
             row.microregion_id, row.microregion_name,
             row.municipality_id, row.municipality_name) = row_data
        elif base_year == 2014:
            (row.state_id, row.state_name,
             row.mesoregion_id, row.mesoregion_name,
             row.microregion_id, row.microregion_name) = row_data[:6]
            row.municipality_id, row.municipality_name = row_data[7:9]
            row.district_id, row.district_name = row_data[10:12]
            row.subdistrict_id, row.subdistrict_name = row_data[13:15]

        return row.normalize(**normalization_options)
