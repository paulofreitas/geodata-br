#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Universal Binary JSON encoder module."""
# Imports

# Built-in dependencies

import ubjson

# Package dependencies

from geodatabr.core import encoders, types
from geodatabr.dataset import serializers

# Classes


class UniversalBinaryJsonFormat(encoders.EncoderFormat):
    """Encoder format class for Universal Binary JSON file format."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        return 'ubjson'

    @property
    def friendlyName(self) -> str:
        """Gets the encoder format friendly name."""
        return 'UBJSON'

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        return '.ubj'

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        return 'Data Interchange'

    @property
    def mimeType(self) -> str:
        """Gets the encoder format media type."""
        return 'application/ubjson'

    @property
    def info(self) -> str:
        """Gets the encoder format reference info."""
        return 'https://en.wikipedia.org/wiki/UBJSON'

    @property
    def isBinary(self) -> bool:
        """Tells whether the encoder format is binary or not."""
        return True


class UniversalBinaryJsonEncoder(encoders.Encoder):
    """
    Universal Binary JSON encoder class.

    Attributes:
        format (geodatabr.encoders.ubjson.UniversalBinaryJsonFormat):
            The encoder format class
        serializer (geodatabr.dataset.serializers.Serializer):
            The encoder serialization class
    """

    format = UniversalBinaryJsonFormat
    serializer = serializers.Serializer

    def encode(self, data: dict, **options) -> types.BinaryFileStream:
        """
        Encodes the data into a Universal Binary JSON file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            A Universal Binary JSON file-like stream

        Raises:
            geodatabr.core.encoders.EncodeError: If data fails to encode
        """
        try:
            return types.BinaryFileStream(
                ubjson.dumpb(data, **dict(self.options, **options)))
        except Exception:
            raise encoders.EncodeError
