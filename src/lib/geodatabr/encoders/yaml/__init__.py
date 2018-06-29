#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""YAML encoder module."""
# Imports

# External dependencies

import yaml

# Package dependencies

from geodatabr.core import encoders
from geodatabr.core.utils import io
from geodatabr.encoders.yaml import utils

# Classes


class YamlFormat(encoders.EncoderFormat):
    """Encoder format class for YAML file format."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        return 'yaml'

    @property
    def friendlyName(self) -> str:
        """Gets the encoder format friendly name."""
        return 'YAML'

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        return '.yaml'

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        return 'Data Interchange'

    @property
    def mimeType(self) -> str:
        """Gets the encoder format media type."""
        return 'application/x-yaml'

    @property
    def info(self) -> str:
        """Gets the encoder format reference info."""
        return 'https://en.wikipedia.org/wiki/YAML'


class YamlEncoder(encoders.Encoder):
    """
    YAML encoder class.

    Attributes:
        format (geodatabr.encoders.yaml.YamlFormat): The encoder format class
    """

    format = YamlFormat

    @property
    def options(self) -> dict:
        """Gets the default encoding options."""
        return dict(allow_unicode=True,
                    default_flow_style=False)

    def encode(self, data: dict, **options) -> io.BinaryFileStream:
        """
        Encodes the data into a YAML file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            A YAML file-like stream

        Raises:
            geodatabr.core.encoders.EncodeError: If data fails to encode
        """
        try:
            utils.register_representers()

            return io.BinaryFileStream(
                yaml.dump(data, **dict(self.options, **options))
                .encode('utf-8'))
        except Exception:
            raise encoders.EncodeError
