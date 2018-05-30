#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
CSV file format utils module
'''
# Imports

# Built-in dependencies

from csv import DictWriter
from sys import version_info

# Classes


class UnicodeDictWriter(DictWriter, object):
    '''
    A custom Unicode dictionary writer for Python 2.7.
    '''

    def __init__(self, csvfile, fieldnames, **kwargs):
        '''
        Constructor.

        Arguments:
            csvfile (file): The file object to write
            fieldnames (collections.abc.Sequence): The CSV header field names
        '''
        super().__init__(csvfile, fieldnames, **kwargs)

    def writerow(self, row):
        '''
        Writes the given row to the writer's file object.

        Arguments:
            row (collections.abc.Mapping): The row object
        '''
        return super().writerow({
            key: value.encode('utf-8') if isinstance(value, unicode) else value
            for key, value in iter(row.items())
        })

    def writerows(self, rows):
        '''
        Writes all the given rows to the writer's file object.

        Arguments:
            rows (list): A list of row objects
        '''
        for row in rows:
            self.writerow(row)


# Enhancements

if version_info < (3, 0):
    DictWriter = UnicodeDictWriter
