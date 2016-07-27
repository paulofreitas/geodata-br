#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
PHP Serialized Data file exporter module
'''
from __future__ import absolute_import

# Imports

# External dependencies

import phpserialize

# Package dependencies

from dtb.exporters import Exporter
from dtb.formats.php_serialized import PhpSerializedFormat

# Classes


class PhpSerializedExporter(Exporter):
    '''PHP Serialized Data exporter class.'''

    # Exporter format
    _format = PhpSerializedFormat

    @property
    def data(self):
        '''Formatted PHP Serialized Data representation of data.'''
        data = self._data.toDict()

        return phpserialize.dumps(data)
