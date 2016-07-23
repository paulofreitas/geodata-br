#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Brazilian territorial distribution data

The MIT License (MIT)

Copyright (c) 2013-2016 Paulo Freitas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
# Classes


class Struct(dict):
    '''A dictionary object which can access/assign/delete keys with attributes.'''

    def __getattr__(self, key):
        '''Magic method to allow accessing dictionary keys as attributes.

        :param key: the dictionary key to access'''
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        '''Magic method to allow assigning dictionary keys with attributes.

        :param key: the dictionary key to change
        :param value: the value to set'''
        self[key] = value

    def __delattr__(self, key):
        '''Magic method to allow deleting dictionary keys with attributes.

        :param key: the dictionary key to delete'''
        del self[key]

    def copy(self):
        '''Copies the self data into a new Struct instance.'''
        return self.__class__(dict.copy(self))
