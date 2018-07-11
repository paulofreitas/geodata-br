#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""XML encoder module."""
# Imports

# External dependencies

from lxml import etree

# Package dependencies

from geodatabr.core import encoders, i18n
from geodatabr.core.utils import io
from geodatabr.dataset import schema

# Classes


class XmlFormat(encoders.EncoderFormat):
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
    def mimeType(self) -> str:
        """Gets the encoder format media type."""
        return 'application/xml'

    @property
    def info(self) -> str:
        """Gets the encoder format reference info."""
        return 'https://en.wikipedia.org/wiki/XML'


class XmlEncoder(encoders.Encoder):
    """
    XML encoder class.

    Attributes:
        format (geodatabr.encoders.xml.XmlFormat): The encoder format class
    """

    format = XmlFormat

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

    def encode(self, data, **options) -> io.BinaryFileStream:
        """
        Encodes the data into a XML file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            A XML file-like stream

        Raises:
            geodatabr.core.encoders.EncodeError: If data fails to encode
        """
        # pylint: disable=protected-access
        try:
            dataset = etree.Element(i18n._('dataset_name'))
            entities = {i18n._(entity.__table__.name): i18n._(entity._name)
                        for entity in schema.ENTITIES}

            for table_name, rows in iter(data.items()):
                table = etree.SubElement(dataset, table_name)

                for row in rows:
                    etree.SubElement(table, entities.get(table_name), row)

            xml_data = etree.tostring(dataset,
                                      **dict(self.options, **options))

            # Workaround for hard-coded single quoting
            xml_declaration = xml_data[:xml_data.find(b'?>') + 2]
            xml_data = xml_data.replace(xml_declaration,
                                        xml_declaration.replace(b"'", b'"'))

            return io.BinaryFileStream(xml_data)
        except Exception:
            raise encoders.EncodeError
