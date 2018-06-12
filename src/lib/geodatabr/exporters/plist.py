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

from geodatabr.dataset.serializers import Serializer
from geodatabr.exporters import Exporter
from geodatabr.formats.plist import PlistFormat
from geodatabr.formats.plist.utils import PlistDumper, BinaryFormat

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
            io.BytesIO: A Property List file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        data = Serializer(forceStrKeys=True).serialize()
        plist_data = PlistDumper(data,
                                 fmt=BinaryFormat,
                                 sort_keys=False)

        return io.BytesIO(plist_data)
