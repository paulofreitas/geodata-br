#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
JSON file exporter module
'''
# Imports

# Built-in dependencies

import io
import json

# Package dependencies

from geodatabr.exporters import Exporter
from geodatabr.formats.json import JsonFormat

# Classes


class JsonExporter(Exporter):
    '''
    JSON exporter class.
    '''

    # Exporter format
    _format = JsonFormat

    def export(self, **options):
        '''
        Exports the data into a JSON file-like stream.

        Arguments:
            options (dict): The exporting options

        Returns:
            io.StringIO: A JSON file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        data = self._data.normalize()
        json_data = json.dumps(data,
                               indent=2,
                               separators=(',', ': '),
                               ensure_ascii=False)

        return io.StringIO(json_data)
