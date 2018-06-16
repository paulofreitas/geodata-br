#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Microsoft Excel Spreadsheet file encoder module."""
# Imports

# External dependencies

from xlwt import Workbook

# Package dependencies

from geodatabr.core.types import BinaryFileStream
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
    Microsoft Excelt Spreadsheet encoder class.

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
            workbook = Workbook(encoding='utf-8')

            for entity, records in data.items():
                sheet = workbook.add_sheet(entity)
                row_id = 0

                for record in records:
                    if row_id == 0:
                        for col_id, (column, _) in enumerate(record.items()):
                            sheet.write(row_id, col_id, column)

                        row_id += 1

                    for col_id, (_, value) in enumerate(record.items()):
                        sheet.write(row_id, col_id, value)

                    row_id += 1

            workbook.save(xls_file)
            xls_file.seek(0)

            return xls_file
        except Exception:
            raise EncodeError
