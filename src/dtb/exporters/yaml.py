#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
YAML file exporter module
'''
from __future__ import absolute_import, unicode_literals

# Imports

# Built-in dependencies

import collections

# External dependencies

import yaml

# Package dependencies

from dtb.exporters import Exporter
from dtb.formats.yaml import YamlFormat

# Enhancements


def __represent_odict(dump, tag, mapping, flow_style=None):
    '''Make PyYAML output an OrderedDict.
    Credits: https://gist.github.com/miracle2k/3184458/
    '''
    value = []
    node = yaml.MappingNode(tag, value, flow_style=flow_style)

    if dump.alias_key is not None:
        dump.represented_objects[dump.alias_key] = node

    best_style = True

    if hasattr(mapping, 'items'):
        mapping = mapping.items()

    for item_key, item_value in mapping:
        node_key = dump.represent_data(item_key)
        node_value = dump.represent_data(item_value)

        if not (isinstance(node_key, yaml.ScalarNode) and not node_key.style):
            best_style = False

        if not (isinstance(node_value, yaml.ScalarNode)
                and not node_value.style):
            best_style = False

        value.append((node_key, node_value))

        if flow_style is None:
            if dump.default_flow_style is not None:
                node.flow_style = dump.default_flow_style
            else:
                node.flow_style = best_style

    return node


yaml.SafeDumper.add_representer(
    collections.OrderedDict,
    lambda dumper, value:
        __represent_odict(dumper, 'tag:yaml.org,2002:map', value)
)


# Classes


class YamlExporter(Exporter):
    '''YAML exporter class.'''

    # Exporter format
    _format= YamlFormat

    @property
    def data(self):
        '''Formatted YAML representation of data.'''
        data = self._data.toDict()
        yaml_opts = dict(default_flow_style=False)

        if self._minified:
            yaml_opts.update(default_flow_style=True, width=2e6, indent=0)

        yaml_str = yaml.safe_dump(data, **yaml_opts)

        if self._minified:
            yaml_str = yaml_str.replace('}, ', '},')

        return yaml_str
