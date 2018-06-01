#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Generic Data File file format module
'''
# Imports

# Package dependencies

from geodatabr.core.helpers.decorators import classproperty
from geodatabr.formats import Format

# Classes


class DatFormat(Format):
    '''
    The file format class for Generic Data File file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'dat'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'Generic Data File'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.dat'

    @classproperty
    def type(self):
        '''
        The file format type.
        '''
        return 'Data'

    @classproperty
    def mimeType(self):
        '''
        The file format media type.
        '''
        return None

    @classproperty
    def isParseable(self):
        '''
        Tells whether the file format is parseable or not.
        '''
        return True
