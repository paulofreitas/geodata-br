#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''YAML encoder utils module.'''
# Imports

# Built-in dependencies

from collections import OrderedDict

# External dependencies

import yaml

# Package dependencies

from geodatabr.core.types import List, Map, OrderedMap

# Monkey patches

for dumper in (yaml.Dumper, yaml.SafeDumper):
    yaml.add_representer(List, dumper.represent_list)

    for mapping in (Map, OrderedDict, OrderedMap):
        yaml.add_representer(mapping, dumper.represent_dict)
