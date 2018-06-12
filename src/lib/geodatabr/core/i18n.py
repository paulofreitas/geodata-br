#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Core internationalization module

This module provides the internationalization facilities.
'''
# External dependencies

import yaml

# Package dependencies

from geodatabr.core.constants import SRC_DIR
from geodatabr.core.helpers.filesystem import File
from geodatabr.core.helpers.decorators import cachedmethod
from geodatabr.core.types import Map

# Classes


class Translation(object):
    '''
    Translation class.
    '''

    def __init__(self, locale_file, domain=None):
        '''
        Constructor.

        Arguments:
            locale_file (geodatabr.core.helpers.filesystem.File): The localization file
            domain (str): An optional domain to load the translations
        '''
        if not isinstance(locale_file, File):
            raise UnsupportedLocaleError('Unsupported localization')

        self._locale = str(locale_file.basename)
        self._domain = domain
        self._translations = Map(yaml.load(locale_file.read()))
        self._domains = self._translations.keys()

        if domain in self._domains:
            self._translations = self._translations.get(domain)

    @property
    def locale(self):
        '''
        Returns the translation localization name.

        Returns:
            str: The translation localization name
        '''
        return self._locale

    @property
    def domain(self):
        '''
        Returns the translation domain name.

        Returns:
            str: The translation domain name
        '''
        return self._domain

    @property
    def domains(self):
        '''
        Returns the list of available translation domain names.

        Returns:
            list: The list of available translation domain names
        '''
        return self._domains

    @cachedmethod()
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
        return {locale_file.basename: locale_file
                for locale_file in cls.LANGUAGE_DIR.files(pattern='*.yaml')}

    @classmethod
    def domains(cls, locale):
        '''
        Returns the available domains for the given localization.

        Arguments:
            locale (str): The localization name

        Returns:
            list: The available localization domain names

        Raises:
            UnsupportedLocaleError: When an unsupported localization is used
        '''
        locale_file = cls.locales().get(locale)

        if not locale_file:
            raise UnsupportedLocaleError('Unsupported localization')

        return Translation(locale_file).domains

    @classmethod
    def translations(cls, domain):
        '''
        Returns the available localizations for the given domain.

        Arguments:
            domain (str): The localization domain name

        Returns:
            dict: The available localizations mapping
        '''
        return {locale: locale_file
                for locale, locale_file in cls.locales().items()
                if domain in Translation(locale_file).domains}

    @classmethod
    def load(cls, domain):
        '''
        Loads the given localization domain.

        Arguments:
            domain (str): The localization domain
        '''
        cls._translations = {
            locale: Translation(locale_file, domain)
            for locale, locale_file in cls.translations(domain).items()}

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
        if cls.locale in cls._translations:
            return cls._translations[cls.locale] \
                .translate(message, **placeholders)

        # Try using the fallback locale
        if cls.fallbackLocale in cls._translations:
            return cls._translations[cls.fallbackLocale] \
                .translate(message, **placeholders)

        # Fallback to the original message
        return message.format(**placeholders)


class UnsupportedLocaleError(Exception):
    '''
    Exception class raised when an unsupported localization is used.
    '''
    pass

# Alias functions

_ = Translator.translate
