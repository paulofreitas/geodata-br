#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
MessagePack file encoder module
'''
# Imports

# External dependencies

import io
import msgpack

# Package dependencies

from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder
from geodatabr.formats.msgpack import MessagePackFormat

# Classes


class MessagePackEncoder(Encoder):
    '''
    MessagePack encoder class.
    '''

    # Encoder format
    _format = MessagePackFormat

    def encode(self, **options):
        '''
        Encodes the data into a MessagePack file-like stream.

        Arguments:
            options (dict): The encoding options

        Returns:
            io.BytesIO: A MessagePack file-like stream

        Raises:
            geodatabr.encoders.EncodeError: When data fails to encode
        '''
        unpacked = Serializer().serialize()
        packed = msgpack.packb(unpacked, use_bin_type=False)

        return io.BytesIO(packed)
