#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""OpenDocument Spreadsheet file encoder module."""
# Imports

# External dependencies

from pyexcel_ods import save_data as write_ods

# Package dependencies

from geodatabr.core.types import BinaryFileStream, OrderedMap
from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder, EncoderFormat, EncodeError

# Classes


class OpenDocumentSpreadsheetFormat(EncoderFormat):
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


class OpenDocumentSpreadsheetEncoder(Encoder):
    """
    OpenDocument Spreadsheet encoder class.

    Attributes:
        format (geodatabr.encoders.ods.OpenDocumentSpreadsheet):
            The encoder format class
        serializer (geodatabr.dataset.serializers.Serializer):
            The encoder serialization class
    """

    format = OpenDocumentSpreadsheetFormat
    serializer = Serializer

    def encode(self, data: dict, **options) -> BinaryFileStream:
        """
        Encodes the data into a OpenDocument Spreadsheet file-like stream.

        Arguments:
            data: The data to encode
            **options: The encoding options

        Returns:
            An OpenDocument Spreadsheet file-like stream

        Raises:
            geodatabr.encoders.EncodeError: If data fails to encode
        """
        try:
            ods_file = BinaryFileStream()
            ods_data = OrderedMap()

            for entity, records in data.items():
                ods_data[entity] = [list(data[entity].first().keys())] \
                    + [list(item.values()) for item in data[entity]]

            write_ods(ods_file, ods_data)
            ods_file.seek(0)

            return ods_file
        except Exception:
            raise EncodeError
