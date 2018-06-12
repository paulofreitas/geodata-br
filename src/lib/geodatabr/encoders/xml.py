#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
XML file encoder module
'''
# Imports

# Built-in dependencies

import io

# External dependencies

from lxml.etree import Comment, Element, SubElement, tostring as xml_str

# Package dependencies

from geodatabr.core.i18n import _, Translator
from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder
from geodatabr.formats.xml import XmlFormat

# Translator setup

Translator.load('dataset')

# Classes


class XmlEncoder(Encoder):
    '''
    XML encoder class.
    '''

    # Encoder format
    _format = XmlFormat

    def encode(self, **options):
        '''
        Encodes the data into a XML file-like stream.

        Arguments:
            options (dict): The encoding options

        Returns:
            io.StringIO: A XML file-like stream

        Raises:
            geodatabr.encoders.EncodeError: When data fails to encode
        '''
        data = Serializer(forceStr=True, includeKey=True).serialize()
        database = Element('database', name=_('dataset_name'))

        for table_name, rows in iter(data.items()):
            database.append(Comment(' Table {} '.format(table_name)))
            table = SubElement(database, 'table', name=table_name)

            for row_data in iter(rows.values()):
                row = SubElement(table, 'row')

                for column_name, column_value in iter(row_data.items()):
                    SubElement(row, 'field', name=column_name).text =\
                        column_value

        xml_data = xml_str(database,
                           xml_declaration=True,
                           encoding='utf-8',
                           pretty_print=True)

        return io.StringIO(xml_data.decode())
