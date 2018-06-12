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

from geodatabr.core.helpers.decorators import classproperty
from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import Encoder, Format
from geodatabr.encoders.plist.utils import PlistDumper, BinaryFormat

# Classes


class PlistFormat(Format):
    '''
    The file format class for Property List file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'plist'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'Property List'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.plist'

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
        return 'application/x-plist'

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/Property_list'

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
