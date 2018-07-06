#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""SQLite encoder module."""
# Imports

# Built-in dependencies

import sqlite3
import tempfile

# Package dependencies

from geodatabr.core import encoders
from geodatabr.core.utils import io
from geodatabr.encoders import sql

# Classes


class SqliteFormat(encoders.EncoderFormat):
    """Encoder format class for SQLite file format."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        return 'sqlite'

    @property
    def friendlyName(self) -> str:
        """Gets the encoder format friendly name."""
        return 'SQLite'

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        return '.sqlite'

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        return 'Database'

    @property
    def mimeType(self) -> str:
        """Gets the encoder format media type."""
        return 'application/vnd.sqlite3'

    @property
    def info(self) -> str:
        """Gets the encoder format reference info."""
        return 'https://en.wikipedia.org/wiki/SQLite'

    @property
    def isBinary(self) -> bool:
        """Tells whether the file format is binary or not."""
        return True


class SqliteEncoder(sql.SqlEncoder, encoders.Encoder):
    """
    SQLite encoder class.

    Attributes:
        format (geodatabr.encoders.sqlite.SqliteFormat):
            The encoder format class
    """

    format = SqliteFormat

    @property
    def options(self) -> dict:
        """Gets the default encoding options."""
        return dict(dialect='sqlite')

    def encode(self, data: dict, **options) -> io.BinaryFileStream:
        """
        Encodes the data into a SQLite file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            A SQLite file-like stream

        Raises:
            geodatabr.core.encoders.EncodeError: If data fails to encode
        """
        try:
            sql_data = super().encode(data, **dict(self.options, **options))

            with tempfile.NamedTemporaryFile() as sqlite_file:
                with sqlite3.connect(sqlite_file.name) as sqlite_con:
                    sqlite_cursor = sqlite_con.cursor()
                    sqlite_cursor.execute('PRAGMA page_size = 1024')
                    sqlite_cursor.execute('PRAGMA foreign_keys = ON')
                    sqlite_cursor.executescript(
                        'BEGIN; {} COMMIT'.format(sql_data.read().decode()))

                return io.BinaryFileStream(sqlite_file.read())
        except Exception:
            raise encoders.EncodeError
