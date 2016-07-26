#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Microsoft Excel Spreadsheet file format module
'''
from __future__ import absolute_import

# Imports

# Package dependencies

from dtb.formats import Format

# Classes


class XlsFormat(Format):
    '''The file format class for Microsoft Excel Spreadsheet file format.'''

    @property
    def name(self):
        '''The file format name.'''
        return 'xls'

    @property
    def friendlyName(self):
        '''The file format friendly name.'''
        return 'Microsoft Excel Spreadsheet'

    @property
    def extension(self):
        '''The file format extension.'''
        return '.xls'

    @property
    def type(self):
        '''The file format type.'''
        return 'Spreadsheet'

    @property
    def mimeType(self):
        '''The file format media type.'''
        return 'application/vnd.ms-excel'

    @property
    def info(self):
        '''The file format reference info.'''
        return 'https://en.wikipedia.org/wiki/Microsoft_Excel_file_format'

    def isBinary(self):
        '''Tells whether the file format is binary or not.'''
        return True

    def isParseable(self):
        '''Tells whether the file format is parseable or not.'''
        return True
