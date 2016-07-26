#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
PHP Serialized Data file format module
'''
from __future__ import absolute_import

# Imports

# Package dependencies

from dtb.formats import Format

# Classes


class PhpSerializedFormat(Format):
    '''The file format class for PHP Serialized Data file format.'''

    @property
    def name(self):
        '''The file format name.'''
        return 'php'

    @property
    def friendlyName(self):
        '''The file format friendly name.'''
        return 'PHP Serialized Data'

    @property
    def extension(self):
        '''The file format extension.'''
        return '.php.serialized'

    @property
    def type(self):
        '''The file format type.'''
        return 'Data Interchange'

    @property
    def mimeType(self):
        '''The file format media type.'''
        return 'application/vnd.php.serialized'

    @property
    def info(self):
        '''The file format reference info.'''
        return 'https://en.wikipedia.org/wiki/Serialization#Programming_language_support'

    def isExportable(self):
        '''Tells whether the file format is exportable or not.'''
        return True
