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

from geodatabr.core.helpers.decorators import classproperty
from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder, Format

# Classes


class MessagePackFormat(Format):
    '''
    The file format class for MessagePack file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'msgpack'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'MessagePack'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.msgpack'

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
        return 'application/x-msgpack'

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/MessagePack'

    @classproperty
    def isBinary(self):
        '''
        Tells whether the file format is binary or not.
        '''
        return True

    @classproperty
    def isExportable(self):
        '''
        Tells whether the file format is exportable or not.
        '''
        return True


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
