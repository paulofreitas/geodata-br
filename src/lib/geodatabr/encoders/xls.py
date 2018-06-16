#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Microsoft Excel Spreadsheet file encoder module."""
# Imports

# External dependencies

from pyexcel_xls import save_data as write_xls

# Package dependencies

from geodatabr.core.types import BinaryFileStream, OrderedMap
from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder, EncoderFormat, EncodeError

# Classes


class MicrosoftExcelFormat(EncoderFormat):
    """Encoder format class for Microsoft Excel Spreadsheet file format."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        return 'xls'

    @property
    def friendlyName(self) -> str:
        """Gets the encoder format friendly name."""
        return 'Microsoft Excel Spreadsheet'

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        return '.xls'

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        return 'Spreadsheet'

    @property
    def mimeType(self) -> str:
        """Gets the encoder format media type."""
        return 'application/vnd.ms-excel'

    @property
    def info(self) -> str:
        """Gets the encoder format reference info."""
        return 'https://en.wikipedia.org/wiki/Microsoft_Excel_file_format'

    @property
    def isBinary(self) -> bool:
        """Tells whether the file format is binary or not."""
        return True


class MicrosoftExcelEncoder(Encoder):
    """
    Microsoft Excel Spreadsheet encoder class.

    Attributes:
        format (geodatabr.encoders.xls.MicrosoftExcelFormat):
            The encoder format class
        serializer (geodatabr.dataset.serializers.Serializer):
            The encoder serialization class
    """

    format = MicrosoftExcelFormat
    serializer = Serializer

    def encode(self, data: dict, **options) -> BinaryFileStream:
        """
        Encodes the data into a Microsoft Excel Spreadsheet file-like stream.

        Arguments:
            data: The data to encode
            **options: The encoding options

        Returns:
            A Microsoft Excel Spreadsheet file-like stream

        Raises:
            geodatabr.encoders.EncodeError: If data fails to encode
        """
        try:
            xls_file = BinaryFileStream()
            xls_data = OrderedMap()

            for entity, records in data.items():
                xls_data[entity] = [list(data[entity].first().keys())] \
                    + [list(item.values()) for item in data[entity]]

            write_xls(xls_file, xls_data)
            xls_file.seek(0)

            return xls_file
        except Exception:
            raise EncodeError
