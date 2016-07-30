#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
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

from dtb.exporters import Exporter
from dtb.formats.csv import CsvFormat

# Classes


class CsvExporter(Exporter):
    '''CSV exporter class.'''

    # Exporter format
    _format = CsvFormat

    @property
    def data(self):
        '''Formatted CSV representation of data.'''
        csv_data = io.BytesIO()
        csv_writer = csv.writer(
            csv_data,
            quoting=(csv.QUOTE_NONNUMERIC, csv.QUOTE_MINIMAL)[self._minified],
            lineterminator='\n'
        )

        csv_writer.writerow(self._data._cols)

        for row in self._data._rows:
            csv_writer.writerow([
                str(col.encode('utf-8')) if isinstance(col, unicode) else col
                for col in row
                if col is not None
            ])

        return csv_data.getvalue()
