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

from dtb.formats import Format

# Classes


class FirebirdFormat(Format):
    '''The file format class for Firebird Embedded file format.'''

    @property
    def name(self):
        '''The file format name.'''
        return 'firebird'

    @property
    def friendlyName(self):
        '''The file format friendly name.'''
        return 'Firebird Embedded'

    @property
    def extension(self):
        '''The file format extension.'''
        return '.fdb'

    @property
    def type(self):
        '''The file format type.'''
        return 'Database'

    @property
    def mimeType(self):
        '''The file format media type.'''
        return None

    @property
    def info(self):
        '''The file format reference info.'''
        return 'https://en.wikipedia.org/wiki/Embedded_database#Firebird_Embedded'

    def isBinary(self):
        '''Tells whether the file format is binary or not.'''
        return True

    def isExportable(self):
        '''Tells whether the file format is exportable or not.'''
        return True
