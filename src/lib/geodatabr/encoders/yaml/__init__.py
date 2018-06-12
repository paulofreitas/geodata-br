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

from geodatabr.core.helpers.decorators import classproperty
from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder, EncoderFormat
from geodatabr.encoders.yaml.utils import OrderedDumper

# Classes


class YamlFormat(EncoderFormat):
    '''
    The file format class for YAML file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'yaml'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'YAML'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.yaml'

    @classproperty
    def type(self):
        '''
        The file format type.
        '''
        return 'Data Interchange'

    @classproperty
    def mimeType(self):
        '''
        The file format media type.
        '''
        return None

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/YAML'


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
