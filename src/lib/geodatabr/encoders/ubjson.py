#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Universal Binary JSON encoder module."""
# Imports

# Built-in dependencies

import ubjson

# Package dependencies

from geodatabr.core.encoders import Encoder, EncoderFormat, EncodeError
from geodatabr.core.types import BinaryFileStream
from geodatabr.dataset.serializers import Serializer

# Classes


class UniversalBinaryJsonFormat(EncoderFormat):
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


class UniversalBinaryJsonEncoder(Encoder):
    """
    Universal Binary JSON encoder class.

    Attributes:
        format (geodatabr.encoders.ubjson.UniversalBinaryJsonFormat):
            The encoder format class
        serializer (geodatabr.dataset.serializers.Serializer):
            The encoder serialization class
    """

    format = UniversalBinaryJsonFormat
    serializer = Serializer

    def encode(self, data: dict, **options) -> BinaryFileStream:
        """
        Encodes the data into a Universal Binary JSON file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            A Universal Binary JSON file-like stream

        Raises:
            geodatabr.encoders.EncodeError: If data fails to encode
        """
        try:
            return BinaryFileStream(
                ubjson.dumpb(data, **dict(self.options, **options)))
        except Exception:
            raise EncodeError
