#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
YAML file encoder module
'''
# Imports

# Built-in dependencies

import io

# External dependencies

import yaml

# Package dependencies

from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder
from geodatabr.formats.yaml import YamlFormat
from geodatabr.formats.yaml.utils import OrderedDumper

# Classes


class YamlEncoder(Encoder):
    '''
    YAML encoder class.
    '''

    # Encoder format
    _format = YamlFormat

    def encode(self, **options):
        '''
        Encodes the data into a YAML file-like stream.

        Arguments:
            options (dict): The encoding options

        Returns:
            io.StringIO: A YAML file-like stream

        Raises:
            geodatabr.encoders.EncodeError: When data fails to encode
        '''
        data = Serializer().serialize()
        yaml_data = yaml.dump(data,
                              Dumper=OrderedDumper,
                              allow_unicode=True,
                              default_flow_style=False)

        return io.StringIO(yaml_data)
