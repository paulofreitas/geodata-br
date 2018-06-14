#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''YAML encoder module.'''
# Imports

# External dependencies

import yaml

# Package dependencies

import geodatabr.encoders.yaml.utils

from geodatabr.core.types import FileStream
from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder, EncoderFormat, EncodeError

# Classes


class YamlFormat(EncoderFormat):
    '''Encoder format class for YAML file format.'''

    @property
    def name(self) -> str:
        '''Gets the encoder format name.'''
        return 'yaml'

    @property
    def friendlyName(self) -> str:
        '''Gets the encoder format friendly name.'''
        return 'YAML'

    @property
    def extension(self) -> str:
        '''Gets the encoder format extension.'''
        return '.yaml'

    @property
    def type(self) -> str:
        '''Gets the encoder format type.'''
        return 'Data Interchange'

    @property
    def mimeType(self) -> None:
        '''Gets the encoder format media type.'''
        return None

    @property
    def info(self) -> str:
        '''Gets the encoder format reference info.'''
        return 'https://en.wikipedia.org/wiki/YAML'


class YamlEncoder(Encoder):
    '''
    YAML encoder class.

    Attributes:
        format (geodatabr.encoders.yaml.YamlFormat): The encoder format class
        serializer (geodatabr.dataset.serializers.Serializer):
            The encoder serialization class
    '''

    format = YamlFormat
    serializer = Serializer

    @property
    def options(self) -> dict:
        '''Gets the default encoding options.'''
        return dict(allow_unicode=True,
                    default_flow_style=False)

    def encode(self, data: dict, **options) -> FileStream:
        '''
        Encodes the data into a YAML file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            A YAML file-like stream

        Raises:
            geodatabr.encoders.EncodeError: If data fails to encode
        '''
        try:
            return FileStream(yaml.dump(data,
                                        **dict(self.options, **options)))
        except Exception:
            raise EncodeError
