#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
CSV file encoder module
'''
# Imports

# Built-in dependencies

import csv
import io

from csv import DictWriter

# Package dependencies

from geodatabr.core.helpers.decorators import classproperty
from geodatabr.dataset.serializers import FlattenedSerializer
from geodatabr.encoders import Encoder, Format

# Classes


class CsvFormat(Format):
    '''
    The file format class for CSV file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'csv'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'CSV'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.csv'

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
        return 'text/csv'

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/Comma-separated_values'

    @classproperty
    def isExportable(self):
        '''
        Tells whether the file format is exportable or not.
        '''
        return True


class CsvEncoder(Encoder):
    '''
    CSV encoder class.
    '''

    # Encoder format
    _format = CsvFormat

    def encode(self, **options):
        '''
        Encodes the data into a CSV file-like stream.

        Arguments:
            options (dict): The encoding options

        Returns:
            io.StringIO: A CSV file-like stream

        Raises:
            geodatabr.encoders.EncodeError: When data fails to encode
        '''
        rows = FlattenedSerializer().serialize()
        csv_data = io.StringIO()
        csv_writer = DictWriter(csv_data,
                                rows[-1].keys(),
                                delimiter=options.get('delimiter', ','),
                                quotechar='"',
                                doublequote=True,
                                lineterminator='\r\n',
                                quoting=csv.QUOTE_MINIMAL,
                                extrasaction='ignore')
        csv_writer.writeheader()
        csv_writer.writerows(rows)
        csv_data.seek(0)

        return csv_data
