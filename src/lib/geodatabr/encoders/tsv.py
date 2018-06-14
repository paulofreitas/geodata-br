#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""TSV encoder module."""
# Imports

# Package dependencies

from geodatabr.core.types import FileStream
from geodatabr.dataset.serializers import FlattenedSerializer
from geodatabr.encoders import Encoder, EncoderFormat, EncodeError
from geodatabr.encoders.csv import CsvEncoder

# Classes


class TsvFormat(EncoderFormat):
    """Encoder format class for TSV file format."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        return 'tsv'

    @property
    def friendlyName(self) -> str:
        """Gets the encoder format friendly name."""
        return 'TSV'

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        return '.tsv'

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        return 'Tabular Text'

    @property
    def mimeType(self) -> str:
        """Gets the file format media type.
        """
        return 'text/tab-separated-values'

    @property
    def info(self) -> str:
        """Gets the encoder format reference info.
        """
        return 'https://en.wikipedia.org/wiki/Tab-separated_values'


class TsvEncoder(Encoder):
    """
    TSV encoder class.

    Attributes:
        format (geodatabr.encoders.tsv.TsvFormat): The encoder format class
        serializer (geodatabr.dataset.serializers.FlattenedSerializer):
            The encoder serialization class
    """

    format = TsvFormat
    serializer = FlattenedSerializer

    @property
    def options(self) -> dict:
        """Gets the default encoding options."""
        return dict(delimiter='\t')

    def encode(self, data: list, **options) -> FileStream:
        """
        Encodes the data into a TSV file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            A TSV file-like stream

        Raises:
            geodatabr.encoders.EncodeError: If data fails to encode
        """
        try:
            return CsvEncoder().encode(data, **dict(self.options, **options))
        except Exception:
            raise EncodeError
