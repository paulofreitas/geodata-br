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

from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder
from geodatabr.formats.json import JsonFormat

# Classes


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
