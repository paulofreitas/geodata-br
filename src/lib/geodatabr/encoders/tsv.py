#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
TSV file encoder module
'''
# Imports

# Package dependencies

from geodatabr.core.helpers.decorators import classproperty
from geodatabr.encoders import Encoder, Format
from geodatabr.encoders.csv import CsvEncoder

# Classes


class TsvFormat(Format):
    '''
    The file format class for TSV file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'tsv'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'TSV'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.tsv'

    @classproperty
    def type(self):
        '''
        The file format type.
        '''
        return 'Tabular Text'

    @classproperty
    def mimeType(self):
        '''
        The file format media type.
        '''
        return 'text/tab-separated-values'

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/Tab-separated_values'

    @classproperty
    def isExportable(self):
        '''
        Tells whether the file format is exportable or not.
        '''
        return True


class TsvEncoder(Encoder):
    '''
    TSV encoder class.
    '''

    # Encoder format
    _format = TsvFormat

    def encode(self, **options):
        '''
        Encodes the data into a TSV file-like stream.

        Arguments:
            options (dict): The encoding options

        Returns:
            io.StringIO: A TSV file-like stream

        Raises:
            geodatabr.encoders.EncodeError: When data fails to encode
        '''
        tsv_options = dict(options, delimiter='\t')

        return CsvEncoder().encode(**tsv_options)
