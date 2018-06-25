#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Binary Property List encoder module."""
# Imports

# Built-in dependencies

import plistlib

# Package dependencies

from geodatabr.core import encoders, types
from geodatabr.dataset import serializers

# Classes


class BinaryPropertyListFormat(encoders.EncoderFormat):
    """Encoder format class for Binary Property List file format."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        return 'plist'

    @property
    def friendlyName(self) -> str:
        """Gets the encoder format friendly name."""
        return 'Binary Property List'

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        return '.plist'

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        return 'Data Interchange'

    @property
    def mimeType(self) -> str:
        """Gets the encoder format media type."""
        return 'application/x-plist'

    @property
    def info(self) -> str:
        """Gets the encoder format reference info."""
        return 'https://en.wikipedia.org/wiki/Property_list'

    @property
    def isBinary(self) -> bool:
        """Tells whether the file format is binary or not."""
        return True


class BinaryPropertyListEncoder(encoders.Encoder):
    """
    Binary Property List encoder class.

    Attributes:
        format (geodatabr.encoders.plist.BinaryPropertyListFormat):
            The encoder format class
        serializer (geodatabr.dataset.serializers.Serializer):
            The encoder serialization class
    """

    format = BinaryPropertyListFormat
    serializer = serializers.Serializer

    @property
    def options(self) -> dict:
        """Gets the default encoding options."""
        return dict(fmt=plistlib.PlistFormat.FMT_BINARY,
                    sort_keys=False)

    def encode(self, data: dict, **options) -> types.BinaryFileStream:
        """
        Encodes the data into a Binary Property List file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            A Binary Property List file-like stream

        Raises:
            geodatabr.core.encoders.EncodeError: If data fails to encode
        """
        try:
            return types.BinaryFileStream(
                plistlib.dumps(data, **dict(self.options, **options)))
        except Exception:
            raise encoders.EncodeError
