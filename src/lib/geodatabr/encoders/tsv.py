#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
TSV file encoder module
'''
# Imports

# Package dependencies

from geodatabr.encoders import Encoder
from geodatabr.encoders.csv import CsvEncoder
from geodatabr.formats.tsv import TsvFormat

# Classes


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
