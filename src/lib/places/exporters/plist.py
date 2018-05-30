#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Property List file exporter module
'''
# Imports

# Built-in dependencies

import io

# Package dependencies

from places.exporters import Exporter
from places.formats.plist import PlistFormat
from places.formats.plist.utils import PlistDumper, PlistWriter

# Classes


class PlistExporter(Exporter):
    '''
    Property List exporter class.
    '''

    # Exporter format
    _format = PlistFormat

    def export(self, **options):
        '''
        Exports the data into a Property List file-like stream.

        Arguments:
            options (dict): The exporting options

        Returns:
            io.StringIO: A Property List file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        data = self._data.normalize(strKeys=True)
        plist_data = PlistDumper(data, sort_keys=False).decode()

        return io.StringIO(plist_data)
