#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Documentation helper module

This module provides helper classes to write documentation files.
'''
# Imports

# Built-in dependencies

import json

from collections import OrderedDict

# Package dependencies

from places.core.constants import BASE_DIR, DATA_DIR, SRC_DIR
from places.core.helpers import Number
from places.core.helpers.decorators import cachedmethod
from places.core.helpers.filesystem import File
from places.core.helpers.markup import GithubMarkdown as Markdown
from places.core.i18n import _, Translator
from places.databases import DatabaseRepository
from places.databases.entities import Entities
from places.formats import FormatRepository

# Classes


class DatasetUtils(object):
    @staticmethod
    @cachedmethod
    def getDatasetsByLocale(locale):
        '''
        Returns the datasets available for a given localization.

        Arguments:
            locale (str): The localization name

        Returns:
            collections.OrderedDict: The localization datasets
        '''
        data = OrderedDict()
        Translator.locale = locale

        for dataset in DatabaseRepository.listYears():
            dataset_file = DATA_DIR / locale / dataset / '{}.json'.format(_('dataset'))

            if dataset_file.exists():
                data[dataset] = json.load(File(dataset_file))

        return data


class Readme(object):
    '''
    A README documentation file.
    '''

    def __init__(self, readme_file, stub_file=None):
        '''
        Constructor.

        Arguments:
            readme_file (places.core.helpers.filesystem.File): The README file
            stub_file (places.core.helpers.filesystem.File): The README stub file
        '''
        self._readme_file = readme_file
        self._stub_file = stub_file
        self._stub = self._stub_file.read() if stub_file else ''

    def render(self):
        '''
        Renders the file.
        '''
        raise NotImplementedError

    def write(self):
        '''
        Writes the file to disk.
        '''
        self._readme_file.write(self.render())


class ProjectReadme(Readme):
    '''
    The project README documentation file.
    '''

    def __init__(self):
        '''
        Constructor.
        '''
        readme_file = File(BASE_DIR / 'README.md')
        stub_file = File(SRC_DIR / 'data/stubs/README.stub.md')

        super().__init__(readme_file, stub_file)

        # Setup translator
        Translator.locale = 'pt'
        Translator.load('databases')

    def render(self):
        '''
        Renders the file.
        '''
        return self._stub.format(
            dataset_records=self.renderDatasetRecords().strip(),
            dataset_formats=self.renderDatasetFormats().strip()
        )

    def renderDatasetRecords(self):
        '''
        Renders the available dataset records counts.

        Returns:
            str: The available dataset records counts
        '''
        headers = ['Dataset'] + [
            Markdown.code(entity.__table__.name) for entity in Entities
        ]
        alignment = ['>'] * 7
        datasets = DatasetUtils.getDatasetsByLocale('pt')
        data = [
            [Markdown.bold(dataset)] + [
                '{:,d}'.format(len(datasets[dataset][_(entity.__table__.name)])) \
                    if _(entity.__table__.name) in datasets[dataset] else '-'
                for entity in Entities
            ]
            for dataset in datasets
        ]

        return Markdown.table([headers] + data, alignment)

    def renderDatasetFormats(self):
        '''
        Renders the available dataset formats.

        Returns:
            str: The available dataset formats
        '''
        grouped_formats = FormatRepository.groupExportableFormatsByType()
        markdown = ''

        for format_type, formats in grouped_formats:
            markdown += '\n'.join([
                Markdown.header(format_type, depth=4),
                Markdown.unorderedList([
                    Markdown.link(_format.info, _format.friendlyName)
                    for _format in formats
                ]) + '\n'
            ])

        return markdown

class DatasetReadme(Readme):
    '''
    A dataset README documentation file.
    '''

    def __init__(self, dataset, dataset_dir, locale):
        '''
        Constructor.

        Arguments:
            dataset (places.databases.Database): The dataset instance
            dataset_dir (str): The dataset directory
            locale (str): The dataset localization
        '''
        readme_file = File(dataset_dir / 'README.md')
        stub_file = File(SRC_DIR / 'data/stubs/BASE_README.stub.md')

        super().__init__(readme_file, stub_file)

        self._dataset = dataset
        self._dataset_dir = dataset_dir
        self._locale = locale

        # Setup translator
        Translator.locale = locale
        Translator.load('databases')

    def render(self):
        '''
        Renders the file.
        '''
        return self._stub.format(
            dataset=self._dataset.year,
            dataset_records=self.renderDatasetRecords().strip(),
            dataset_files=self.renderDatasetFiles().strip())

    def renderDatasetRecords(self):
        '''
        Renders the dataset records counts.

        Returns:
            str: The dataset records counts
        '''
        headers = ['Table', 'Records']
        alignment = ['>', '>']
        datasets = DatasetUtils.getDatasetsByLocale(self._locale)
        data = [
            [Markdown.code(_(entity.__table__.name)),
             '{:,d}'.format(len(datasets[self._dataset.year][_(entity.__table__.name)]))]
            for entity in Entities
            if _(entity.__table__.name) in datasets[self._dataset.year]
        ]

        return Markdown.table([headers] + data, alignment)

    def renderDatasetFiles(self):
        '''
        Renders the dataset files info.

        Returns:
            str: The dataset files info
        '''
        headers = ['File', 'Format', 'Size']
        alignment = ['<', '^', '>']
        data = []

        for dataset_file in self._dataset_dir.files(pattern=_('dataset') + '*'):
            dataset_format = '-'

            if dataset_file.format:
                dataset_format = Markdown.link(dataset_file.format.info,
                                               dataset_file.format.friendlyName)

            dataset_info = [
                Markdown.code(dataset_file.name),
                dataset_format,
                '{:9,d}'.format(dataset_file.size),
            ]

            data.append(dataset_info)

        return Markdown.table([headers] + data, alignment)
