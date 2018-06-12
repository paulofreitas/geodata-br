#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Microsoft Excel Spreadsheet file encoder module
'''
# Imports

# Package dependencies

from geodatabr.core.helpers.decorators import classproperty
from geodatabr.encoders import EncoderFormat

# Classes


class XlsFormat(EncoderFormat):
    '''
    The file format class for Microsoft Excel Spreadsheet file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'xls'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'Microsoft Excel Spreadsheet'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.xls'

    @classproperty
    def type(self):
        '''
        The file format type.
        '''
        return 'Spreadsheet'

    @classproperty
    def mimeType(self):
        '''
        The file format media type.
        '''
        return 'application/vnd.ms-excel'

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/Microsoft_Excel_file_format'

    @classproperty
    def isBinary(self):
        '''
        Tells whether the file format is binary or not.
        '''
        return True
