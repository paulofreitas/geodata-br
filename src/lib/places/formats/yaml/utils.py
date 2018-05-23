#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
YAML file format utils module
'''
from __future__ import unicode_literals

# Imports

# Built-in dependencies

import collections

# External compatibility dependencies

from future.utils import iteritems

# External dependencies

import yaml

# Classes


class OrderedDumper(yaml.SafeDumper):
    '''
    A YAML dumper which is able to serialize OrderedDict objects.
    Usage: `yaml.dump(data, Dumper=OrderedDumper)`
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor.
        '''
        super(OrderedDumper, self).__init__(*args, **kwargs)

        self.add_representer(collections.OrderedDict, self.representOrderedDict)

    def representOrderedDict(self, _, mapping):
        '''
        Represents OrderedDict objects.

        Arguments:
            mapping (collections.OrderedDict): The ordered dictionary to render

        Returns:
            yaml.nodes.MappingNode: A YAML mapping node
        '''
        return self.represent_mapping('tag:yaml.org,2002:map',
                                      iteritems(mapping))
