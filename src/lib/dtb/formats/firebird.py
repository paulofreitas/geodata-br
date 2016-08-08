#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Firebird Embedded file format module
'''
from __future__ import absolute_import

# Imports

# Package dependencies

from dtb.core.helpers.decorators import classproperty
from dtb.formats import Format

# Classes


class FirebirdFormat(Format):
    '''
    The file format class for Firebird Embedded file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'firebird'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'Firebird Embedded'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.fdb'

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
        return None

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/Embedded_database#Firebird_Embedded'

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
