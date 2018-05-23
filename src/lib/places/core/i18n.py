#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Core internationalization module

This module provides the internationalization facilities.
'''
from __future__ import unicode_literals

# External dependencies

import yaml

# Package dependencies

from places.core.constants import SRC_DIR
from places.core.helpers.filesystem import File
from places.core.helpers.decorators import cachedmethod
from places.core.types import Map

# Classes


class Translation(object):
    '''
    Translation class.
    '''

    def __init__(self, locale_file):
        '''
        Constructor.

        Arguments:
            locale_file: The localization file
        '''
        if not isinstance(locale_file, File):
            raise UnsupportedLocaleError('Unsupported localization')

        self._locale = str(locale_file.parent)
        self._domain = locale_file.basename
        self._translations = Map(yaml.load(unicode(locale_file.read())))

    @property
    def locale(self):
        '''
        Returns the translation localization.

        Returns:
            str: The translation localization name
        '''
        return self._locale

    @property
    def domain(self):
        '''
        Returns the translation domain.

        Returns:
            str: The translation domain name
        '''
        return self._domain

    @cachedmethod
    def translate(self, message, **placeholders):
        '''
        Translates the given message with their placeholders.

        Arguments:
            message (str): The message to be translated
            placeholders (dict): Any translation placeholder

        Returns:
            str: The translated message
        '''
        if message in self._translations:
            return self._translations.get(message).format(placeholders)

        return message


class Translator(object):
    '''
    Translator service.
    '''

    LANGUAGE_DIR = SRC_DIR / 'data' / 'translations'

    # Default locale
    locale = 'en'

    # Default fallback locale
    fallbackLocale = 'en'

    # Translation instance
    _translation = None

    @classmethod
    def locales(cls):
        '''
        Returns the available localizations.

        Returns:
            dict: The available localizations mapping
        '''
        return {locale_dir.name: locale_dir
                for locale_dir in cls.LANGUAGE_DIR.directories()}

    @classmethod
    def domains(cls, locale):
        '''
        Returns the available domains for the given localization.

        Arguments:
            locale (str): The localization name

        Returns:
            dict: The available localization domains mapping

        Raises:
            UnsupportedLocaleError: When an unsupported localization is used
        '''
        locale_dir = cls.locales().get(locale)

        if not locale_dir:
            raise UnsupportedLocaleError('Unsupported localization')

        return {domain_file.baename: domain_file
                for domain_file in locale_dir.files(pattern='*.yaml')}

    @classmethod
    def translations(cls, domain):
        '''
        Returns the available localizations for the given domain.

        Arguments:
            domain (str): The localization domain

        Returns:
            dict: The available localizations mapping
        '''
        return {locale_dir.name: domain_file
                for locale_dir in cls.LANGUAGE_DIR.directories()
                for domain_file in locale_dir.files(pattern=domain + '.yaml')}

    @classmethod
    def load(cls, domain):
        '''
        Loads the given localization domain.

        Arguments:
            domain (str): The localization domain
        '''
        # Normalize domain name
        if '.' in domain:
            domain = '_'.join(domain.split('.')[1:])

        translations = cls.translations(domain)

        if cls.locale in translations:
            cls._translation = Translation(translations.get(cls.locale))

            return cls._translation

        return

    @classmethod
    def translate(cls, message, **placeholders):
        '''
        Translates the given message with their placeholders.

        Arguments:
            message (str): The message to be translated
            placeholders (dict): Any translation placeholder

        Returns:
            str: The translated message
        '''
        if cls._translation:
            return cls._translation.translate(message, **placeholders)

        # Fallback to the original message
        return message.format(**placeholders)


class UnsupportedLocaleError(Exception):
    '''
    Exception class raised when an unsupported localization is used.
    '''
    pass

# Alias functions

_ = Translator.translate
