#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Brazilian territorial distribution data exporter

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

# -- Imports ------------------------------------------------------------------

# Built-in imports
import os
import sys

# Dependency modules

import xlrd

# Package modules
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

from base import BaseParser
from core.value_objects import Struct

# -- Implementation -----------------------------------------------------------


class XlsParser(BaseParser):
    '''XLS parser class.'''
    format = 'xls'

    def __init__(self, base, logger):
        super(XlsParser, self).__init__(base, logger)

        self._book = xlrd.open_workbook(file_contents=self._data._rawdata,
                                        logfile=open(os.devnull, 'w'))
        self._sheet = self._book.sheet_by_name(self._data._base.sheet)

    def parse(self):
        self._logger.debug('Parsing database...')

        for row_id in xrange(self._sheet.nrows):
            row_data =\
                [value.encode('utf-8') for value in self._sheet.row_values(row_id)]

            if row_id == 0:
                self._data._cols = self._data._cols[:len(row_data)]
                continue

            id_uf, nome_uf, id_mesorregiao, nome_mesorregiao, \
                id_microrregiao, nome_microrregiao, id_municipio, nome_municipio, \
                id_distrito, nome_distrito, id_subdistrito, nome_subdistrito =\
                row_data + [None] * (12 - len(row_data))

            # Normalize data as needed
            if len(id_mesorregiao) == 2:
                id_mesorregiao = id_uf + id_mesorregiao
                id_microrregiao = id_uf + id_microrregiao
                id_municipio = id_uf + id_municipio

                if id_distrito:
                    id_distrito = id_municipio + id_distrito

                if id_subdistrito:
                    id_subdistrito = id_distrito + id_subdistrito

            if len(id_municipio) == 5:
                id_municipio = id_uf + id_municipio

                if id_distrito:
                    id_distrito = id_municipio + id_distrito

                if id_subdistrito:
                    id_subdistrito = id_distrito + id_subdistrito

            if id_distrito:
                if len(id_distrito) == 2:
                    id_distrito = id_municipio + id_distrito

                    if id_subdistrito:
                        id_subdistrito = id_distrito + id_subdistrito

            id_subdistrito = int(id_subdistrito) if id_subdistrito else None
            id_distrito = int(id_distrito) if id_distrito else None
            id_municipio = int(id_municipio)
            id_microrregiao = int(id_microrregiao)
            id_mesorregiao = int(id_mesorregiao)
            id_uf = int(id_uf)

            self._data._rows.append([
                id_uf, nome_uf, id_mesorregiao, nome_mesorregiao,
                id_microrregiao, nome_microrregiao, id_municipio,
                nome_municipio, id_distrito, nome_distrito,
                id_subdistrito if nome_subdistrito else None,
                nome_subdistrito or None
            ])

            # uf
            uf = Struct(
                id=id_uf,
                nome=nome_uf
            )

            if uf not in self._data._dict['uf']:
                self._data._dict['uf'].append(uf)

            # mesorregiao
            mesorregiao = Struct(
                id=id_mesorregiao,
                id_uf=id_uf,
                nome=nome_mesorregiao
            )

            if mesorregiao not in self._data._dict['mesorregiao']:
                self._data._dict['mesorregiao'].append(mesorregiao)

            # microrregiao
            microrregiao = Struct(
                id=id_microrregiao,
                id_mesorregiao=id_mesorregiao,
                id_uf=id_uf,
                nome=nome_microrregiao
            )

            if microrregiao not in self._data._dict['microrregiao']:
                self._data._dict['microrregiao'].append(microrregiao)

            # municipio
            municipio = Struct(
                id=id_municipio,
                id_microrregiao=id_microrregiao,
                id_mesorregiao=id_mesorregiao,
                id_uf=id_uf,
                nome=nome_municipio
            )

            if municipio not in self._data._dict['municipio']:
                self._data._dict['municipio'].append(municipio)

            # distrito
            if id_distrito:
                distrito = Struct(
                    id=id_distrito,
                    id_municipio=id_municipio,
                    id_microrregiao=id_microrregiao,
                    id_mesorregiao=id_mesorregiao,
                    id_uf=id_uf,
                    nome=nome_distrito
                )

                if distrito not in self._data._dict['distrito']:
                    self._data._dict['distrito'].append(distrito)

            # subdistrito
            if nome_subdistrito:
                subdistrito = Struct(
                    id=id_subdistrito,
                    id_distrito=id_distrito,
                    id_municipio=id_municipio,
                    id_microrregiao=id_microrregiao,
                    id_mesorregiao=id_mesorregiao,
                    id_uf=id_uf,
                    nome=nome_subdistrito
                )

                if subdistrito not in self._data._dict['subdistrito']:
                    self._data._dict['subdistrito'].append(subdistrito)

        # Sort data
        for table in self._data._dict:
            self._data._dict[table] = sorted(
                self._data._dict[table],
                key=lambda row: row['id']
            )

        return self._data
