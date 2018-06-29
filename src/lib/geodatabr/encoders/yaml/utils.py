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


def register_representers():
    """Registers custom YAML representers."""
    for dumper in (yaml.Dumper, yaml.SafeDumper):
        yaml.add_representer(types.List, dumper.represent_list)

        for mapping in (collections.OrderedDict, types.Map, types.OrderedMap):
            yaml.add_representer(mapping, dumper.represent_dict)
