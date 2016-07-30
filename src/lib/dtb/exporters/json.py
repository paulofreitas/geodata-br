#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
JSON file exporter module
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

import json

# Package dependencies

from dtb.exporters import Exporter
from dtb.formats.json import JsonFormat

# Classes


class JsonExporter(Exporter):
    '''JSON exporter class.'''

    # Exporter format
    _format = JsonFormat

    @property
    def data(self):
        '''Formatted JSON representation of data.'''
        data = self._data.toDict()
        json_opts = dict(indent=2)

        if self._minified:
            json_opts = dict(separators=(',', ':'))

        json_str = json.dumps(data, **json_opts)

        return json_str
