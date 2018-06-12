#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
JSON file encoder module
'''
# Imports

# Built-in dependencies

import io
import json

# Package dependencies

from geodatabr.core.helpers.decorators import classproperty
from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder, Format

# Classes


class JsonFormat(Format):
    '''
    The file format class for JSON file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'json'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'JSON'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.json'

    @classproperty
    def type(self):
        '''
        The file format type.
        '''
        return 'Data Interchange'

    @classproperty
    def mimeType(self):
        '''
        The file format media type.
        '''
        return 'application/json'

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/JSON'

    @classproperty
    def isExportable(self):
        '''
        Tells whether the file format is exportable or not.
        '''
        return True


class JsonEncoder(Encoder):
    '''
    JSON encoder class.
    '''

    # Encoder format
    _format = JsonFormat

    def encode(self, **options):
        '''
        Encodes the data into a JSON file-like stream.

        Arguments:
            options (dict): The encoding options

        Returns:
            io.StringIO: A JSON file-like stream

        Raises:
            geodatabr.encoders.EncodeError: When data fails to encode
        '''
        data = Serializer().serialize()
        json_data = json.dumps(data,
                               indent=2,
                               separators=(',', ': '),
                               ensure_ascii=False)

        return io.StringIO(json_data)
