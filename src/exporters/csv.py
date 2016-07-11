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

# -- Imports ------------------------------------------------------------------

from __future__ import absolute_import

# Built-in modules

import csv
import io

# Package modules

from .base import BaseExporter

# -- Implementation -----------------------------------------------------------


class CsvExporter(BaseExporter):
    '''CSV exporter class.'''
    format = 'CSV'
    extension = '.csv'

    def __str__(self):
        csv_file = io.BytesIO()
        csv_writer = csv.writer(
            csv_file,
            quoting=(csv.QUOTE_NONNUMERIC, csv.QUOTE_MINIMAL)[self._minified],
            lineterminator='\n'
        )

        csv_writer.writerow([col.encode('utf-8') for col in self._data._cols])

        for row in self._data._rows:
            csv_writer.writerow([
                bytes(col) if type(col) == str else col
                for col in filter(None, row)
            ])

        return csv_file.getvalue()
