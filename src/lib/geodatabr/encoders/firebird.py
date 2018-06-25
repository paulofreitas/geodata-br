#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Firebird Embedded encoder module."""
# Imports

# Built-in dependencies

import tempfile

# External dependencies

import fdb

# Package dependencies

from geodatabr.core import encoders, types
from geodatabr.core.utils import io
from geodatabr.dataset import serializers
from geodatabr.encoders import sql

# Classes


class FirebirdFormat(encoders.EncoderFormat):
    """Encoder format class for Firebird Embedded file format."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        return 'firebird'

    @property
    def friendlyName(self):
        """Gets the encoder format friendly name."""
        return 'Firebird Embedded'

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        return '.fdb'

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        return 'Database'

    @property
    def mimeType(self) -> None:
        """Gets the encoder format media type."""
        return None

    @property
    def info(self) -> str:
        """Gets the encoder format reference info."""
        return 'https://en.wikipedia.org/wiki/Embedded_database#Firebird_Embedded'

    @property
    def isBinary(self) -> bool:
        """Tells whether the file format is binary or not."""
        return True


class FirebirdEncoder(sql.SqlEncoder, encoders.Encoder):
    """
    Firebird encoder class.

    Attributes:
        format (geodatabr.encoders.firebird.FirebirdFormat):
            The encoder format class
        serializer (geodatabr.dataset.serializers.Serializer):
            The encoder serialization class
    """

    format = FirebirdFormat
    serializer = serializers.Serializer

    @property
    def options(self) -> dict:
        """Gets the default encoding options."""
        return dict(dialect='firebird')

    def encode(self, data: dict, **options) -> types.BinaryFileStream:
        """
        Encodes the data into a Firebird Embedded file-like stream.

        Arguments:
            data: The data to encode
            **options: The encoding options

        Returns:
            A Firebird Embedded file-like stream

        Raises:
            geodatabr.core.encoders.EncodeError: If data fails to encode
        """
        try:
            sql_data = super().encode(data, **dict(self.options, **options))
            fdb_file = tempfile.mktemp()
            fdb_con = fdb.create_database(
                "CREATE DATABASE '{}' USER 'sysdba' PASSWORD 'masterkey'"
                .format(fdb_file),
                sql_dialect=3)
            fdb_cursor = fdb_con.cursor()
            in_trans = False

            for stmt in sql_data.read().decode().rstrip(';').split(';'):
                if stmt.startswith('INSERT') and not in_trans:
                    fdb_con.begin()
                    in_trans = True
                else:
                    fdb_con.commit()
                    in_trans = False

                fdb_cursor.execute(stmt)

            return types.BinaryFileStream(io.File(fdb_file).readBytes())
        except Exception:
            raise encoders.EncodeError
