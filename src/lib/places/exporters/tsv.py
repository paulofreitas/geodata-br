#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
TSV file exporter module
'''
# Imports

# Package dependencies

from places.exporters import Exporter
from places.exporters.csv import CsvExporter
from places.formats.tsv import TsvFormat

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
            io.StringIO: A TSV file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        tsv_options = dict(options, delimiter='\t')

        return CsvExporter(self._data).export(**tsv_options)
