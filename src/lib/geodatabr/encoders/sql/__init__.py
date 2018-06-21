#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""SQL encoder module."""
# Imports

# Package dependencies

from geodatabr.core import encoders, types
from geodatabr.dataset import schema, serializers
from geodatabr.encoders.sql import utils as sql_utils

# Classes


class SqlFormat(encoders.EncoderFormat):
    """Encoder format class for SQL file format."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        return 'sql'

    @property
    def friendlyName(self) -> str:
        """Gets the encoder format friendly name."""
        return 'SQL'

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        return '.sql'

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        return 'Database'

    @property
    def mimeType(self) -> str:
        """Gets the encoder format media type."""
        return 'application/sql'

    @property
    def info(self) -> str:
        """Gets the encoder format reference info."""
        return 'https://en.wikipedia.org/wiki/SQL'


class SqlEncoder(encoders.Encoder):
    """
    SQL encoder class.

    Attributes:
        format (geodatabr.encoders.sql.SqlFormat): The encoder format class
        serializer (geodatabr.dataset.serializers.Serializer):
            The encoder serialization class
    """

    format = SqlFormat
    serializer = serializers.Serializer

    @property
    def options(self) -> dict:
        """Gets the default encoding options."""
        return dict(dialect='default')

    @property
    def serializationOptions(self) -> dict:
        """Gets the encoder serialization options."""
        return dict(localize=False)

    def encode(self, data: dict, **options) -> types.FileStream:
        """
        Encodes the data into a SQL file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            A SQL file-like stream

        Raises:
            geodatabr.core.encoders.EncodeError: If data fails to encode
        """
        try:
            sql_schema = sql_utils.SchemaGenerator(**dict(self.options,
                                                          **options))

            for entity in schema.ENTITIES:
                records = data.get(entity.__table__.name)

                if records:
                    sql_schema.addTable(entity.__table__, records)

            return types.FileStream(sql_schema.render())
        except Exception:
            raise encoders.EncodeError
