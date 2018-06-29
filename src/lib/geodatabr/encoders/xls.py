#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Microsoft Excel Spreadsheet file encoder module."""
# Imports

# External dependencies

import pyexcel_xls

# Package dependencies

from geodatabr.core import encoders, types
from geodatabr.core.utils import io

# Classes


class MicrosoftExcelFormat(encoders.EncoderFormat):
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


class MicrosoftExcelEncoder(encoders.Encoder):
    """
    Microsoft Excel Spreadsheet encoder class.

    Attributes:
        format (geodatabr.encoders.xls.MicrosoftExcelFormat):
            The encoder format class
    """

    format = MicrosoftExcelFormat

    def encode(self, data: dict, **options) -> io.BinaryFileStream:
        """
        Encodes the data into a Microsoft Excel Spreadsheet file-like stream.

        Arguments:
            data: The data to encode
            **options: The encoding options

        Returns:
            A Microsoft Excel Spreadsheet file-like stream

        Raises:
            geodatabr.core.encoders.EncodeError: If data fails to encode
        """
        try:
            xls_file = io.BinaryFileStream()
            xls_data = types.OrderedMap()

            for entity, records in data.items():
                xls_data[entity] = [list(records.first().keys())] \
                    + [list(record.values()) for record in records]

            pyexcel_xls.save_data(xls_file, xls_data)
            xls_file.seek(0)

            return xls_file
        except Exception:
            raise encoders.EncodeError
