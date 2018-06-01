#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
CSV file exporter module
'''
# Imports

# Built-in dependencies

import csv
import io

# Package dependencies

from geodatabr.exporters import Exporter
from geodatabr.formats.csv import CsvFormat
from geodatabr.formats.csv.utils import DictWriter

# Classes


class CsvExporter(Exporter):
    '''
    CSV exporter class.
    '''

    # Exporter format
    _format = CsvFormat

    def export(self, **options):
        '''
        Exports the data into a CSV file-like stream.

        Arguments:
            options (dict): The exporting options

        Returns:
            io.StringIO: A CSV file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        csv_data = io.StringIO()
        csv_writer = DictWriter(csv_data,
                                self._data.columns,
                                delimiter=options.get('delimiter', ','),
                                quotechar='"',
                                doublequote=True,
                                lineterminator='\r\n',
                                quoting=csv.QUOTE_MINIMAL,
                                extrasaction='ignore')

        csv_writer.writeheader()
        csv_writer.writerows([row.serialize() for row in self._data.rows])
        csv_data.seek(0)

        return csv_data
