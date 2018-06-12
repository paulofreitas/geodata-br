#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
SQL file encoder module
'''
# Imports

# Built-in dependencies

import io

# Package dependencies

from geodatabr.dataset.schema import Entities
from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder
from geodatabr.formats.sql import SqlFormat
from geodatabr.formats.sql.utils import SchemaGenerator

# Classes


class SqlEncoder(Encoder):
    '''
    SQL encoder class.
    '''

    # Encoder format
    _format = SqlFormat

    def encode(self, **options):
        '''
        Encodes the data into a SQL file-like stream.

        Arguments:
            options (dict): The encoding options

        Returns:
            io.StringIO: A SQL file-like stream

        Raises:
            geodatabr.encoders.EncodeError: When data fails to encode
        '''
        data = Serializer(localize=False, includeKey=True).serialize()
        schema = SchemaGenerator(options.get('dialect', 'default'))

        for entity in Entities:
            records = data.get(entity.__table__.name)

            if records:
                schema.addTable(entity.__table__, records)

        return io.StringIO(schema.render())
