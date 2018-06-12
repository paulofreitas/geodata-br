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

from geodatabr.core.helpers.decorators import classproperty
from geodatabr.dataset.schema import Entities
from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder, Format
from geodatabr.encoders.sql.utils import SchemaGenerator

# Classes


class SqlFormat(Format):
    '''
    The file format class for SQL file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'sql'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'SQL'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.sql'

    @classproperty
    def type(self):
        '''
        The file format type.
        '''
        return 'Database'

    @classproperty
    def mimeType(self):
        '''
        The file format media type.
        '''
        return 'application/sql'

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/SQL'

    @classproperty
    def isExportable(self):
        '''
        Tells whether the file format is exportable or not.
        '''
        return True


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
