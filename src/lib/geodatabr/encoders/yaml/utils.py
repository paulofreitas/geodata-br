#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
YAML file format utils module
'''
# Imports

# Built-in dependencies

from collections import OrderedDict

# External dependencies

import yaml

# Package dependencies

from geodatabr.core.types import Map, OrderedMap

# Classes


class OrderedDumper(yaml.Dumper):
    '''
    A YAML dumper which is able to serialize ordered mapping objects.
    Usage: `yaml.dump(data, Dumper=OrderedDumper)`
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor.
        '''
        super().__init__(*args, **kwargs)

        for mapping in (OrderedDict, Map, OrderedMap):
            yaml.add_representer(mapping, self._mappingRepresenter)
            yaml.add_representer(mapping, self._mappingRepresenter,
                                 Dumper=yaml.SafeDumper)

    def _mappingRepresenter(self, dumper, mapping):
        '''
        Represents mapping objects.

        Arguments:
            dumper (yaml.dumper.BaseDumper): The YAML dumper to use
            mapping (collections.MutableMapping): The mapping to represent

        Returns:
            yaml.nodes.MappingNode: A YAML mapping node
        '''
        return dumper.represent_dict(mapping.items())
