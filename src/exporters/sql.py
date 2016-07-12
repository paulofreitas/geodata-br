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

from __future__ import absolute_import

# Built-in modules

import collections

# Package modules

from .base import BaseExporter

# -- Implementation -----------------------------------------------------------


class SqlExporter(BaseExporter):
    '''SQL exporter class.'''
    format = 'SQL'
    extension = '.sql'

    def __table(self, table_name, *args):
        '''Makes table creation statements.'''
        if self._minified:
            return 'CREATE TABLE {}({});'.format(table_name, ','.join(args))

        return '\n'.join([
            'CREATE TABLE {} ('.format(table_name),
            ',\n'.join(args),
            ');\n',
        ])

    def __column(self, column_name, column_type):
        '''Makes column definition statements.'''
        if self._minified:
            return '{} {}'.format(column_name, column_type)

        return '  {} {}'.format(column_name, column_type)

    def __primaryKey(self, table, column):
        '''Makes primary key constraints statements.'''
        pk_name = 'pk_{}'.format(table)

        # If not using column constraints
        if self._lazy_constraints:
            if self._minified:
                return 'ALTER TABLE {} ADD CONSTRAINT {} PRIMARY KEY({});' \
                    .format(table, pk_name, column)

            return '\n'.join([
                'ALTER TABLE {}'.format(table),
                '  ADD CONSTRAINT {}'.format(pk_name),
                '    PRIMARY KEY ({});'.format(column),
            ])

        if self._minified:
            return ' CONSTRAINT {} PRIMARY KEY({})'.format(pk_name, column)

        return '\n'.join([
            '  CONSTRAINT {}'.format(pk_name),
            '    PRIMARY KEY ({})'.format(column),
        ])

    def __foreignKey(self, table, column, foreign_table, foreign_column):
        '''Makes foreign key constraints statements.'''
        fk_name = 'fk_{}_{}'.format(table, foreign_table)

        # If not using column constraints
        if self._lazy_constraints:
            if self._minified:
                return 'ALTER TABLE {} ADD CONSTRAINT {} FOREIGN KEY({}) REFERENCES {}({});' \
                    .format(table, fk_name, column, foreign_table, foreign_column)

            return '\n'.join([
                'ALTER TABLE {}'.format(table),
                '  ADD CONSTRAINT {}'.format(fk_name),
                '    FOREIGN KEY ({})'.format(column),
                '      REFERENCES {} ({});'.format(foreign_table, foreign_column),
            ])

        if self._minified:
            return 'CONSTRAINT {} FOREIGN KEY ({}) REFERENCES {}({})' \
                .format(fk_name, column, foreign_table, foreign_column)

        return '\n'.join([
            '  CONSTRAINT {}'.format(fk_name),
            '    FOREIGN KEY ({})'.format(column),
            '      REFERENCES {} ({})'.format(foreign_table, foreign_column),
        ])

    def __constraints(self, *constraints):
        '''Makes all constraints statements.'''
        if self._minified:
            return ''.join(constraints)

        return '\n'.join(constraints) + '\n'

    def __index(self, index_name, table_name, indexed_column):
        '''Makes index creation statements.'''
        if self._minified:
            return 'CREATE INDEX {} ON {}({});' \
                .format(index_name, table_name, indexed_column)

        return 'CREATE INDEX {} ON {} ({});' \
            .format(index_name, table_name, indexed_column)

    def __indexes(self, *indexes):
        '''Makes all indexes statements.'''
        if self._minified:
            return ''.join(indexes)

        return '\n'.join(indexes) + '\n'

    def __insert(self, table_name, *columns):
        '''Makes insert statements.'''
        if self._minified:
            return 'INSERT INTO {} VALUES({});' \
                .format(table_name, ','.join(columns))

        return 'INSERT INTO {} VALUES ({});\n' \
            .format(table_name, ', '.join(columns))

    def __insertField(self, field_name, field_type):
        repl_field = '{' + field_name + '}'

        return repr(repl_field) if field_type == str else repl_field

    def __quote(self, value):
        '''Quotes values using the right escape char.'''
        return value.replace("'", self._escape_char)

    def __init__(self, base, minified, dialect='standard'):
        super(SqlExporter, self).__init__(base, minified)

        # Standard settings
        self._lazy_constraints = True
        self._create_indexes = True
        self._bigint_type = 'BIGINT'
        self._escape_char = "\\'"

        # Handle dialect settings
        if dialect == 'sqlite':
            self._lazy_constraints = False
            self._escape_char = "''"

        # SQL data
        self._tables = {
            'uf': [
                self.__column('id', 'SMALLINT NOT NULL'),
                self.__column('nome', 'VARCHAR(32) NOT NULL')
            ],
            'mesorregiao': [
                self.__column('id', 'SMALLINT NOT NULL'),
                self.__column('id_uf', 'SMALLINT NOT NULL'),
                self.__column('nome', 'VARCHAR(64) NOT NULL')
            ],
            'microrregiao': [
                self.__column('id', 'INTEGER NOT NULL'),
                self.__column('id_mesorregiao', 'SMALLINT NOT NULL'),
                self.__column('id_uf', 'SMALLINT NOT NULL'),
                self.__column('nome', 'VARCHAR(64) NOT NULL')
            ],
            'municipio': [
                self.__column('id', 'INTEGER NOT NULL'),
                self.__column('id_microrregiao', 'INTEGER NOT NULL'),
                self.__column('id_mesorregiao', 'SMALLINT NOT NULL'),
                self.__column('id_uf', 'SMALLINT NOT NULL'),
                self.__column('nome', 'VARCHAR(64) NOT NULL')
            ],
            'distrito': [
                self.__column('id', 'INTEGER NOT NULL'),
                self.__column('id_municipio', 'INTEGER NOT NULL'),
                self.__column('id_microrregiao', 'INTEGER NOT NULL'),
                self.__column('id_mesorregiao', 'SMALLINT NOT NULL'),
                self.__column('id_uf', 'SMALLINT NOT NULL'),
                self.__column('nome', 'VARCHAR(64) NOT NULL')
            ],
            'subdistrito': [
                self.__column('id', '{} NOT NULL'.format(self._bigint_type)),
                self.__column('id_distrito', 'INTEGER NOT NULL'),
                self.__column('id_municipio', 'INTEGER NOT NULL'),
                self.__column('id_microrregiao', 'INTEGER NOT NULL'),
                self.__column('id_mesorregiao', 'SMALLINT NOT NULL'),
                self.__column('id_uf', 'SMALLINT NOT NULL'),
                self.__column('nome', 'VARCHAR(64) NOT NULL')
            ]
        }
        self._constraints = {
            'uf': [
                self.__primaryKey('uf', 'id')
            ],
            'mesorregiao': [
                self.__primaryKey('mesorregiao', 'id'),
                self.__foreignKey('mesorregiao', 'id_uf', 'uf', 'id')
            ],
            'microrregiao': [
                self.__primaryKey('microrregiao', 'id'),
                self.__foreignKey(
                    'microrregiao', 'id_mesorregiao', 'mesorregiao', 'id'
                ),
                self.__foreignKey('microrregiao', 'id_uf', 'uf', 'id')
            ],
            'municipio': [
                self.__primaryKey('municipio', 'id'),
                self.__foreignKey(
                    'municipio', 'id_microrregiao', 'microrregiao', 'id'
                ),
                self.__foreignKey(
                    'municipio', 'id_mesorregiao', 'mesorregiao', 'id'
                ),
                self.__foreignKey('municipio', 'id_uf', 'uf', 'id')
            ],
            'distrito': [
                self.__primaryKey('distrito', 'id'),
                self.__foreignKey(
                    'distrito', 'id_municipio', 'municipio', 'id'
                ),
                self.__foreignKey(
                    'distrito', 'id_microrregiao', 'microrregiao', 'id'
                ),
                self.__foreignKey(
                    'distrito', 'id_mesorregiao', 'mesorregiao', 'id'
                ),
                self.__foreignKey('distrito', 'id_uf', 'uf', 'id')
            ],
            'subdistrito': [
                self.__primaryKey('subdistrito', 'id'),
                self.__foreignKey(
                    'subdistrito', 'id_distrito', 'distrito', 'id'
                ),
                self.__foreignKey(
                    'subdistrito', 'id_municipio', 'municipio', 'id'
                ),
                self.__foreignKey(
                    'subdistrito', 'id_microrregiao', 'microrregiao', 'id'
                ),
                self.__foreignKey(
                    'subdistrito', 'id_mesorregiao', 'mesorregiao', 'id'
                ),
                self.__foreignKey('subdistrito', 'id_uf', 'uf', 'id')
            ]
        }
        self._indexes = {
            'mesorregiao': [
                self.__index('fk_mesorregiao_uf', 'mesorregiao', 'id_uf')
            ],
            'microrregiao': [
                self.__index(
                    'fk_microrregiao_mesorregiao',
                    'microrregiao',
                    'id_mesorregiao'
                ),
                self.__index('fk_microrregiao_uf', 'microrregiao', 'id_uf')
            ],
            'municipio': [
                self.__index(
                    'fk_municipio_microrregiao', 'municipio', 'id_microrregiao'
                ),
                self.__index(
                    'fk_municipio_mesorregiao', 'municipio', 'id_mesorregiao'
                ),
                self.__index('fk_municipio_uf', 'municipio', 'id_uf')
            ],
            'distrito': [
                self.__index(
                    'fk_distrito_municipio', 'distrito', 'id_municipio'
                ),
                self.__index(
                    'fk_distrito_microrregiao', 'distrito', 'id_microrregiao'
                ),
                self.__index(
                    'fk_distrito_mesorregiao', 'distrito', 'id_mesorregiao'
                ),
                self.__index('fk_distrito_uf', 'distrito', 'id_uf')
            ],
            'subdistrito': [
                self.__index(
                    'fk_subdistrito_distrito', 'subdistrito', 'id_distrito'
                ),
                self.__index(
                    'fk_subdistrito_municipio', 'subdistrito', 'id_municipio'
                ),
                self.__index(
                    'fk_subdistrito_microrregiao',
                    'subdistrito',
                    'id_microrregiao'
                ),
                self.__index(
                    'fk_subdistrito_mesorregiao',
                    'subdistrito',
                    'id_mesorregiao'
                ),
                self.__index('fk_subdistrito_uf', 'subdistrito', 'id_uf')
            ]
        }
        self._inserts = {
            'uf': [
                self.__insertField('id', int),
                self.__insertField('nome', str)
            ],
            'mesorregiao': [
                self.__insertField('id', int),
                self.__insertField('id_uf', int),
                self.__insertField('nome', str)
            ],
            'microrregiao': [
                self.__insertField('id', int),
                self.__insertField('id_mesorregiao', int),
                self.__insertField('id_uf', int),
                self.__insertField('nome', str)
            ],
            'municipio': [
                self.__insertField('id', int),
                self.__insertField('id_microrregiao', int),
                self.__insertField('id_mesorregiao', int),
                self.__insertField('id_uf', int),
                self.__insertField('nome', str)
            ],
            'distrito': [
                self.__insertField('id', int),
                self.__insertField('id_municipio', int),
                self.__insertField('id_microrregiao', int),
                self.__insertField('id_mesorregiao', int),
                self.__insertField('id_uf', int),
                self.__insertField('nome', str)
            ],
            'subdistrito': [
                self.__insertField('id', int),
                self.__insertField('id_distrito', int),
                self.__insertField('id_municipio', int),
                self.__insertField('id_microrregiao', int),
                self.__insertField('id_mesorregiao', int),
                self.__insertField('id_uf', int),
                self.__insertField('nome', str)
            ]
        }

    def __str__(self):
        sql = ''

        for table_name in self._data._tables:
            if not self._data._dict[table_name]:
                continue

            if not self._minified:
                sql += '''
--
-- Structure for table "{}"
--
'''.format(table_name)

            cols = self._tables[table_name] if self._lazy_constraints \
                else self._tables[table_name] + self._constraints[table_name]

            sql += self.__table(table_name, *cols)

            if not self._minified:
                sql += '''
--
-- Data for table "{}"
--
'''.format(table_name)

            for item in self._data._dict[table_name]:
                data = collections.OrderedDict()

                for key in self._data._fields[table_name]:
                    data[key] = item[key] if type(item[key]) == int \
                        else self.__quote(item[key])

                sql += self.__insert(table_name, *self._inserts[table_name]) \
                    .format(**data)

            if self._lazy_constraints:
                if not self._minified:
                    sql += '''
--
-- Constraints for table "{}"
--
'''.format(table_name)

                sql += self.__constraints(*self._constraints[table_name])

            if self._create_indexes:
                if table_name in self._indexes:
                    if not self._minified:
                        sql += '''
--
-- Indexes for table "{}"
--
'''.format(table_name)

                    sql += self.__indexes(*self._indexes[table_name])

        sql = sql.strip()

        return sql
