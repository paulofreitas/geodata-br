#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Office Open XML Workbook file encoder module."""
# Imports

# External dependencies

from pyexcel_xlsx import save_data as write_xlsx

# Package dependencies

from geodatabr.core.types import BinaryFileStream, OrderedMap
from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder, EncoderFormat, EncodeError

# Classes


class OfficeOpenXmlWorkbookFormat(EncoderFormat):
    """Encoder format class for Office Open XML Workbook file format."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        return 'xlsx'

    @property
    def friendlyName(self) -> str:
        """Gets the encoder format friendly name."""
        return 'Office Open XML Workbook'

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        return '.xlsx'

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        return 'Spreadsheet'

    @property
    def mimeType(self) -> str:
        """Gets the encoder format media type."""
        return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    @property
    def info(self) -> str:
        """Gets the encoder format reference info."""
        return 'https://en.wikipedia.org/wiki/Office_Open_XML'

    @property
    def isBinary(self) -> bool:
        """Tells whether the file format is binary or not."""
        return True


class OfficeOpenXmlWorkbookEncoder(Encoder):
    """
    Office Open XML Workbook encoder class.

    Attributes:
        format (geodatabr.encoders.xlsx.OfficeOpenXmlWorkbookFormat):
            The encoder format class
        serializer (geodatabr.dataset.serializers.Serializer):
            The encoder serialization class
    """

    format = OfficeOpenXmlWorkbookFormat
    serializer = Serializer

    def encode(self, data: dict, **options) -> BinaryFileStream:
        """
        Encodes the data into a Office Open XML Workbook file-like stream.

        Arguments:
            data: The data to encode
            **options: The encoding options

        Returns:
            A Office Open XML Workbook file-like stream

        Raises:
            geodatabr.encoders.EncodeError: If data fails to encode
        """
        try:
            xlsx_file = BinaryFileStream()
            xlsx_data = OrderedMap()

            for entity, records in data.items():
                xlsx_data[entity] = [list(records.first().keys())] \
                    + [list(record.values()) for record in records]

            write_xlsx(xlsx_file, xlsx_data)
            xlsx_file.seek(0)

            return xlsx_file
        except Exception:
            raise EncodeError
