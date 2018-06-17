#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""XML encoder module."""
# Imports

# External dependencies

from lxml.etree import Element, SubElement, tostring as xml_str

# Package dependencies

from geodatabr.core.i18n import _
from geodatabr.core.types import FileStream
from geodatabr.dataset.schema import Entities
from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder, EncoderFormat, EncodeError

# Classes


class XmlFormat(EncoderFormat):
    """Encoder format class for XML file format."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        return 'xml'

    @property
    def friendlyName(self) -> str:
        """Gets the encoder format friendly name."""
        return 'XML'

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        return '.xml'

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        return 'Data Interchange'

    @property
    def mimeType(self) -> list:
        """Gets the encoder format media type."""
        return ['application/xml', 'text/xml']

    @property
    def info(self) -> str:
        """Gets the encoder format reference info."""
        return 'https://en.wikipedia.org/wiki/XML'


class XmlEncoder(Encoder):
    """
    XML encoder class.

    Attributes:
        format (geodatabr.encoders.xml.XmlFormat): The encoder format class
        serializer (geodatabr.dataset.serializers.Serializer):
            The encoder format serialization class
    """

    format = XmlFormat
    serializer = Serializer

    @property
    def options(self) -> dict:
        """Gets the default encoding options."""
        return dict(xml_declaration=True,
                    encoding='utf-8',
                    pretty_print=True)

    @property
    def serializationOptions(self) -> dict:
        """Gets the encoder serialization options."""
        return dict(forceStr=True)

    def encode(self, data, **options) -> FileStream:
        """
        Encodes the data into a XML file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            A XML file-like stream

        Raises:
            geodatabr.encoders.EncodeError: If data fails to encode
        """
        try:
            dataset = Element(_('dataset_name'))
            entities = {_(entity.__table__.name): _(entity._name)
                        for entity in Entities}

            for table_name, rows in iter(data.items()):
                table = SubElement(dataset, table_name)

                for row in rows:
                    SubElement(table, entities.get(table_name), row)

            xml_data = xml_str(dataset, **dict(self.options, **options))

            # Workaround for hard-coded single quoting
            xml_declaration = xml_data[:xml_data.find(b'?>') + 2]
            xml_data = xml_data.replace(xml_declaration,
                                        xml_declaration.replace(b"'", b'"'))

            return FileStream(xml_data.decode())
        except Exception:
            raise EncodeError
