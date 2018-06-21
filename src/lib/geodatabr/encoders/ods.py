#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""OpenDocument Spreadsheet file encoder module."""
# Imports

# External dependencies

import pyexcel_ods

# Package dependencies

from geodatabr.core import encoders, types
from geodatabr.dataset import serializers

# Classes


class OpenDocumentSpreadsheetFormat(encoders.EncoderFormat):
    """Encoder format class for OpenDocument Spreadsheet file format."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        return 'ods'

    @property
    def friendlyName(self) -> str:
        """Gets the encoder format friendly name."""
        return 'OpenDocument Spreadsheet'

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        return '.ods'

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        return 'Spreadsheet'

    @property
    def mimeType(self) -> str:
        """Gets the encoder format media type."""
        return 'application/vnd.oasis.opendocument.spreadsheet'

    @property
    def info(self) -> str:
        """Gets the encoder format reference info."""
        return 'https://en.wikipedia.org/wiki/OpenDocument'

    @property
    def isBinary(self) -> bool:
        """Tells whether the file format is binary or not."""
        return True


class OpenDocumentSpreadsheetEncoder(encoders.Encoder):
    """
    OpenDocument Spreadsheet encoder class.

    Attributes:
        format (geodatabr.encoders.ods.OpenDocumentSpreadsheet):
            The encoder format class
        serializer (geodatabr.dataset.serializers.Serializer):
            The encoder serialization class
    """

    format = OpenDocumentSpreadsheetFormat
    serializer = serializers.Serializer

    def encode(self, data: dict, **options) -> types.BinaryFileStream:
        """
        Encodes the data into a OpenDocument Spreadsheet file-like stream.

        Arguments:
            data: The data to encode
            **options: The encoding options

        Returns:
            An OpenDocument Spreadsheet file-like stream

        Raises:
            geodatabr.core.encoders.EncodeError: If data fails to encode
        """
        try:
            ods_file = types.BinaryFileStream()
            ods_data = types.OrderedMap()

            for entity, records in data.items():
                ods_data[entity] = [list(records.first().keys())] \
                    + [list(record.values()) for record in records]

            pyexcel_ods.save_data(ods_file, ods_data)
            ods_file.seek(0)

            return ods_file
        except Exception:
            raise encoders.EncodeError
