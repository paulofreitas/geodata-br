#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
YAML file exporter module
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

import io
import re

# External dependencies

import yaml

# Package dependencies

from places.exporters import Exporter
from places.formats.yaml import YamlFormat
from places.formats.yaml.utils import OrderedDumper

# Classes


class YamlExporter(Exporter):
    '''
    YAML exporter class.
    '''

    # Exporter format
    _format = YamlFormat

    def export(self, **options):
        '''
        Exports the data into a YAML file-like stream.

        Arguments:
            options (dict): The exporting options

        Returns:
            io.BytesIO: A YAML file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        data = self._data.normalize(forceUnicode=True)
        yaml_data = yaml.dump(data,
                              Dumper=OrderedDumper,
                              allow_unicode=True,
                              default_flow_style=False)

        return io.BytesIO(yaml_data)
