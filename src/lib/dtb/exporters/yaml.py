#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
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

from dtb.exporters import Exporter
from dtb.formats.yaml import YamlFormat
from dtb.formats.yaml.utils import OrderedDumper

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
        yaml_options = dict(default_flow_style=False)

        if options.get('minify'):
            yaml_options.update(default_flow_style=True,
                                width=2e6,
                                indent=0)

        data = self._data.normalize(forceUnicode=True)
        yaml_data = yaml.dump(data, Dumper=OrderedDumper, **yaml_options)

        if options.get('minify'):
            yaml_data = re.sub('(?<=[,:])\s+', '', yaml_data)

        return io.BytesIO(yaml_data)
