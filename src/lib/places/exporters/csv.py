#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
CSV file exporter module
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

import csv
import io

# Package dependencies

from places.exporters import Exporter
from places.formats.csv import CsvFormat
from places.formats.csv.utils import DictWriter

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
            io.BytesIO: A CSV file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        csv_options = dict(delimiter=options.get('delimiter', ','),
                           quoting=csv.QUOTE_NONNUMERIC,
                           lineterminator='\r\n',
                           extrasaction='ignore')

        if options.get('minify'):
            csv_options.update(quoting=csv.QUOTE_MINIMAL)

        csv_data = io.BytesIO()
        csv_writer = DictWriter(csv_data,
                                self._data.columns,
                                **csv_options)

        csv_writer.writeheader()
        csv_writer.writerows([row.serialize() for row in self._data.rows])
        csv_data.seek(0)

        return csv_data
