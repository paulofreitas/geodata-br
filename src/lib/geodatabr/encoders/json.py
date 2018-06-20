#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""JSON encoder module."""
# Imports

# Built-in dependencies

import json

# Package dependencies

from geodatabr.core.encoders import Encoder, EncoderFormat, EncodeError
from geodatabr.core.types import BinaryFileStream
from geodatabr.dataset.serializers import Serializer

# Classes


class JsonFormat(EncoderFormat):
    """Encoder format class for JSON file format."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        return 'json'

    @property
    def friendlyName(self) -> str:
        """Gets the encoder format friendly name."""
        return 'JSON'

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        return '.json'

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        return 'Data Interchange'

    @property
    def mimeType(self) -> str:
        """Gets the encoder format media type."""
        return 'application/json'

    @property
    def info(self) -> str:
        """Gets the encoder format reference info."""
        return 'https://en.wikipedia.org/wiki/JSON'


class JsonEncoder(Encoder):
    """
    JSON encoder class.

    Attributes:
        format (geodatabr.encoders.json.JsonFormat): The encoder format class
        serializer (geodatabr.dataset.serializers.Serializer):
            The encoder serialization class
    """

    format = JsonFormat
    serializer = Serializer

    @property
    def options(self) -> dict:
        """Gets the default encoding options."""
        return dict(indent=2,
                    separators=(',', ': '),
                    ensure_ascii=False)

    def encode(self, data: dict, **options) -> BinaryFileStream:
        """
        Encodes the data into a JSON file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            A JSON file-like stream

        Raises:
            geodatabr.encoders.EncodeError: If data fails to encode
        """
        try:
            return BinaryFileStream(
                json.dumps(data, **dict(self.options, **options))
                .encode('utf-8'))
        except Exception:
            raise EncodeError
