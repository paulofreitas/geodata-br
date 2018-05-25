#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
MessagePack file format module
'''
from __future__ import absolute_import

# Imports

# Package dependencies

from places.core.helpers.decorators import classproperty
from places.formats import Format

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