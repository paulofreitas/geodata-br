#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Core helpers package

This package provides utility helper modules.
'''
# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2018 Paulo Freitas'
__license__ = 'MIT License'

# Classes


class Number(object):
    @staticmethod
    def percentDifference(from_value, to_value):
        return (1 - float(from_value) / float(to_value)) * 100
