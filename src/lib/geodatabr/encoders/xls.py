#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Microsoft Excel Spreadsheet file encoder module."""
# Imports

# Package dependencies

from geodatabr.encoders import EncoderFormat

# Classes


class XlsFormat(EncoderFormat):
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
