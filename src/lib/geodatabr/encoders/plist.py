#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Property List file encoder module
'''
# Imports

# Built-in dependencies

import io

# Package dependencies

from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder
from geodatabr.formats.plist import PlistFormat
from geodatabr.formats.plist.utils import PlistDumper, BinaryFormat

# Classes


class PropertyListEncoder(Encoder):
    '''
    Property List encoder class.
    '''

    # Encoder format
    _format = PlistFormat

    def encode(self, **options):
        '''
        Encodes the data into a Property List file-like stream.

        Arguments:
            options (dict): The encoding options

        Returns:
            io.BytesIO: A Property List file-like stream

        Raises:
            geodatabr.encoders.EncodeError: When data fails to encode
        '''
        data = Serializer(forceStrKeys=True).serialize()
        plist_data = PlistDumper(data,
                                 fmt=BinaryFormat,
                                 sort_keys=False)

        return io.BytesIO(plist_data)
