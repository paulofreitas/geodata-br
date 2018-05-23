#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
PHP Serialized Data file exporter module
'''
from __future__ import absolute_import

# Imports

# External dependencies

import io
import phpserialize

# Package dependencies

from places.exporters import Exporter
from places.formats.php_serialized import PhpSerializedFormat

# Classes


class PhpSerializedExporter(Exporter):
    '''
    PHP Serialized Data exporter class.
    '''

    # Exporter format
    _format = PhpSerializedFormat

    def export(self, **options):
        '''
        Exports the data into a PHP Serialized Data file-like stream.

        Arguments:
            options (dict): The exporting options

        Returns:
            io.BytesIO: A PHP Serialized Data file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        data = self._data.normalize()
        php_serialized_data = phpserialize.dumps(data)

        return io.BytesIO(php_serialized_data)
