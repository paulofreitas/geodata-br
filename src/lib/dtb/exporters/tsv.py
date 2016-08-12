#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
TSV file exporter module
'''
from __future__ import absolute_import

# Imports

# Package dependencies

from dtb.exporters import Exporter
from dtb.exporters.csv import CsvExporter
from dtb.formats.tsv import TsvFormat

# Classes


class TsvExporter(Exporter):
    '''
    TSV exporter class.
    '''

    # Exporter format
    _format = TsvFormat

    def export(self, **options):
        '''
        Exports the data into a TSV file-like stream.

        Arguments:
            options (dict): The exporting options

        Returns:
            io.BytesIO: A TSV file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        tsv_options = dict(options, delimiter='\t')

        return CsvExporter(self._data).export(**tsv_options)
