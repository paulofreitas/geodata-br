#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""SQLite 3 encoder module."""
# Imports

# Built-in dependencies

import sqlite3
import tempfile

# Package dependencies

from geodatabr.core import encoders, types
from geodatabr.dataset import serializers
from geodatabr.encoders import sql

# Classes


class Sqlite3Format(encoders.EncoderFormat):
    """Encoder format class for SQLite 3 file format."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        return 'sqlite3'

    @property
    def friendlyName(self) -> str:
        """Gets the encoder format friendly name."""
        return 'SQLite 3'

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        return '.sqlite3'

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        return 'Database'

    @property
    def mimeType(self) -> str:
        """Gets the encoder format media type."""
        return 'application/x-sqlite3'

    @property
    def info(self) -> str:
        """Gets the encoder format reference info."""
        return 'https://en.wikipedia.org/wiki/SQLite'

    @property
    def isBinary(self) -> bool:
        """Tells whether the file format is binary or not."""
        return True


class Sqlite3Encoder(sql.SqlEncoder, encoders.Encoder):
    """
    SQLite3 encoder class.

    Attributes:
        format (geodatabr.encoders.sqlite3.Sqlite3Format):
            The encoder format class
        serializer (geodatabr.dataset.serializers.Serializer):
            The encoder serialization class
    """

    format = Sqlite3Format
    serializer = serializers.Serializer

    @property
    def options(self) -> dict:
        """Gets the default encoding options."""
        return dict(dialect='sqlite')

    def encode(self, data: dict, **options) -> types.BinaryFileStream:
        """
        Encodes the data into a SQLite 3 file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            A SQLite 3 file-like stream

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

                return types.BinaryFileStream(sqlite_file.read())
        except Exception:
            raise encoders.EncodeError
