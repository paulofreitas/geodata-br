#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""YAML encoder utils module."""
# Imports

# Built-in dependencies

import collections

# External dependencies

import yaml

# Package dependencies

from geodatabr.core import types

# Functions


def represent_mapping(dumper: yaml.dumper.BaseDumper,
                      mapping: dict,
                      flow_style: bool = None) -> yaml.MappingNode:
    """
    Represents mappings without sorting items.

    Args:
        dumper: The YAML dumper to use
        mapping: The mapping to represent
        flow_style: The mapping flow style

    Returns:
        The YAML mapping node
    """
    value = []
    node = yaml.MappingNode(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                            value,
                            flow_style=flow_style)
    best_style = True

    if dumper.alias_key is not None:
        dumper.represented_objects[dumper.alias_key] = node

    for item_key, item_value in mapping.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        if (not (isinstance(node_key, yaml.ScalarNode) and not node_key.style)
                or not (isinstance(node_value, yaml.ScalarNode)
                        and not node_value.style)):
            best_style = False

        value.append((node_key, node_value))

    if flow_style is None:
        node.flow_style = (dumper.default_flow_style
                           if dumper.default_flow_style is not None
                           else best_style)

    return node


def register_representers():
    """Registers custom YAML representers."""
    for dumper in (yaml.Dumper, yaml.SafeDumper):
        yaml.add_representer(types.List, dumper.represent_list)

        for mapping in (collections.OrderedDict, types.Map, types.OrderedMap):
            yaml.add_representer(mapping, represent_mapping)
