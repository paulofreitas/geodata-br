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

from itertools import groupby

# Package dependencies

from geodatabr.core.constants import BASE_DIR, SRC_DIR
from geodatabr.core.helpers.filesystem import File
from geodatabr.core.helpers.markup import GithubMarkdown as Markdown
from geodatabr.core.i18n import _, Translator
from geodatabr.dataset.serializers import Serializer
from geodatabr.formats import FormatRepository

# Setup translator

Translator.locale = 'en'
Translator.load('dataset')

# Classes


class Readme(object):
    '''
    A README documentation file.
    '''

    def __init__(self, readme_file, stub_file=None):
        '''
        Constructor.

        Arguments:
            readme_file (geodatabr.core.helpers.filesystem.File): The README file
            stub_file (geodatabr.core.helpers.filesystem.File): The README stub file
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

    def render(self):
        '''
        Renders the file.

        Returns:
            str: The rendered project README contents
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
        headers = ['Table/Collection', 'Records']
        alignment = ['>'] * 2
        dataset = Serializer().serialize()
        data = [
            [Markdown.code(entity),
             '{:,d}'.format(len(dataset[entity]))]
            for entity in dataset
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

    def __init__(self, dataset_dir):
        '''
        Constructor.

        Arguments:
            dataset_dir (str): The dataset directory
        '''
        readme_file = File(dataset_dir / 'README.md')
        stub_file = File(SRC_DIR / 'data/stubs/BASE_README.stub.md')

        super().__init__(readme_file, stub_file)

        self._dataset_dir = dataset_dir

    def render(self):
        '''
        Renders the file.

        Returns:
            str: The rendered dataset README contents
        '''
        return self._stub.format(
            dataset_records=self.renderDatasetRecords().strip(),
            dataset_files=self.renderDatasetFiles().strip())

    def renderDatasetRecords(self):
        '''
        Renders the dataset records counts.

        Returns:
            str: The dataset records counts
        '''
        headers = ['Table/Collection', 'Records']
        alignment = ['>', '>']
        dataset = Serializer().serialize()
        data = [
            [Markdown.code(entity),
             '{:,d}'.format(len(dataset[entity]))]
            for entity in dataset
        ]

        return Markdown.table([headers] + data, alignment)

    def renderDatasetFiles(self):
        '''
        Renders the dataset files info.

        Returns:
            str: The dataset files info
        '''
        files = list(self._dataset_dir.files(pattern=_('dataset_name') + '*'))
        grouped_files = groupby(sorted(files, key=lambda file: file.format.type),
                                key=lambda file: file.format.type)
        listing = []

        for dataset_type, dataset_files in grouped_files:
            listing.append(Markdown.header(dataset_type, depth=4))
            headers = ['File', 'Format', 'Size']
            alignment = ['<', '^', '>']
            rows = []

            for dataset_file in dataset_files:
                dataset_format = '-'

                if dataset_file.format:
                    dataset_format = Markdown.link(dataset_file.format.info,
                                                   dataset_file.format.friendlyName)

                rows.append([
                    Markdown.code(dataset_file.name),
                    dataset_format,
                    '{:9,d}'.format(dataset_file.size),
                ])

            listing.append(Markdown.table([headers] + rows, alignment))

        return '\n'.join(listing)
