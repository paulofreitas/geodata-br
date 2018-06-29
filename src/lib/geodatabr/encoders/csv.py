#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""CSV encoder module."""
# Imports

# Built-in dependencies

import csv

# Package dependencies

from geodatabr.core import encoders
from geodatabr.core.utils import io

# Classes


class CsvFormat(encoders.EncoderFormat):
    """Encoder format class for CSV file format."""

    @property
    def name(self):
        """Gets the encoder format name."""
        return 'csv'

    @property
    def friendlyName(self):
        """Gets the encoder format friendly name."""
        return 'CSV'

    @property
    def extension(self):
        """Gets the encoder format extension."""
        return '.csv'

    @property
    def type(self):
        """Gets the encoder format type."""
        return 'Tabular Text'

    @property
    def mimeType(self):
        """Gets the encoder format media type."""
        return 'text/csv'

    @property
    def info(self):
        """Gets the file format reference info."""
        return 'https://en.wikipedia.org/wiki/Comma-separated_values'


class CsvEncoder(encoders.Encoder):
    """
    CSV encoder class.

    Attributes:
        format (geodatabr.encoders.csv.CsvFormat): The encoder format class
    """

    format = CsvFormat

    @property
    def options(self) -> dict:
        """Gets the default encoding options."""
        return dict(delimiter=',',
                    quotechar='"',
                    doublequote=True,
                    lineterminator='\r\n',
                    quoting=csv.QUOTE_MINIMAL,
                    extrasaction='ignore')

    def encode(self, data: list, **options) -> io.BinaryFileStream:
        """
        Encodes the data into a CSV file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            A CSV file-like stream

        Raises:
            geodatabr.core.encoders.EncodeError: If data fails to encode
        """
        try:
            csv_data = io.FileStream()
            csv_writer = csv.DictWriter(csv_data,
                                        data.last().keys(),
                                        **dict(self.options, **options))
            csv_writer.writeheader()
            csv_writer.writerows(data)
            csv_data.seek(0)

            return io.BinaryFileStream(csv_data.getvalue().encode('utf-8'))
        except Exception:
            raise encoders.EncodeError
