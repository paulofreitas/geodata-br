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
from __future__ import absolute_import, unicode_literals

# Imports

# External compatibility dependencies

from builtins import str
from future.utils import iteritems

# External dependencies

from sqlalchemy import dialects
from sqlalchemy.engine import default
from sqlalchemy.exc import CompileError
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import crud
from sqlalchemy.sql.ddl import AddConstraint, CreateColumn, CreateIndex, \
                               CreateTable
from sqlalchemy.sql.dml import Insert
from sqlalchemy.sql.schema import ForeignKeyConstraint, Index, \
                                  PrimaryKeyConstraint

# Package dependencies

from .base import BaseExporter

# Classes


class SchemaGenerator(object):
    '''SQL schema generator class.'''

    minified = False

    def __init__(self, dialect='default', minified=False):
        '''Constructor.

        :param dialect: the SQL dialect to use
        :param minified: whether the SQL statements should be minified or not
        '''
        self.tables = []
        self.dialect = dialect
        self._dialect = self.getDialect(dialect)

        SchemaGenerator.minified = minified

    @staticmethod
    def getDialect(dialect):
        '''Get the given SQL dialect instance by name.'''
        if dialect == 'default':
            return default.DefaultDialect()

        if dialect in ['firebird', 'mssql', 'mysql', 'oracle', 'postgresql',
                       'sqlite', 'sybase']:
            return dialects.registry.load(dialect)

        raise Exception('Unsupported dialect: {}'.format(dialect))

    # Custom DDL/DML compilers

    @staticmethod
    @compiles(CreateColumn)
    def __compileCreateColumn(create, compiler, **kw):
        '''Compiles the CREATE TABLE columns statements.'''
        column = create.element

        ddl = '{} {}'.format(column.name,
                             compiler.type_compiler.process(column.type))

        default_str = compiler.get_column_default_string(column)

        if default_str is not None:
            ddl += ' DEFAULT ' + default_str

        if not column.nullable:
            ddl += ' NOT NULL'

        if column.constraints:
            ddl += ' '.join(compiler.process(constraint)
                            for constraint in column.constraints)

        return ddl

    @staticmethod
    @compiles(CreateTable)
    def __compileCreateTable(create, compiler, **kw):
        '''Compiles the CREATE TABLE statements.'''
        table = create.element
        separator = '' if SchemaGenerator.minified else '\n'
        first_pk = False

        ddl = 'CREATE '

        if table._prefixes:
            ddl += ' '.join(table._prefixes) + ' '

        ddl += 'TABLE ' + compiler.preparer.format_table(table)
        ddl += '(' if SchemaGenerator.minified else ' ('

        for create_column in create.columns:
            column = create_column.element

            try:
                column_ddl = compiler.process(
                    create_column,
                    first_pk=column.primary_key and not first_pk
                )

                if column_ddl is not None:
                    ddl += separator
                    separator = ',' if SchemaGenerator.minified else ',\n'

                    if not SchemaGenerator.minified:
                        ddl += '  '

                    ddl += column_ddl

                if column.primary_key:
                    first_pk = True
            except CompileError:
                pass

        constraints_ddl = compiler.create_table_constraints(
            table,
            _include_foreign_key_constraints=
                create.include_foreign_key_constraints
        )

        if constraints_ddl:
            ddl += ',' if SchemaGenerator.minified else ',\n  '
            ddl += constraints_ddl.replace(
                ', \n\t',
                ',' if SchemaGenerator.minified else ',\n  '
            )

        if not SchemaGenerator.minified:
            ddl += '\n'

        ddl += '){};'.format(compiler.post_create_table(table))

        return ddl

    @staticmethod
    @compiles(CreateIndex)
    def __compileCreateIndex(create,
                             compiler,
                             include_schema=False,
                             include_table_schema=True):
        '''Compiles CREATE INDEX statements.'''
        index = create.element

        compiler._verify_index_table(index)

        ddl = 'CREATE '
        separator = ',' if SchemaGenerator.minified else ', '

        if index.unique:
            ddl += 'UNIQUE '

        ddl += 'INDEX {} ON {}'.format(
            compiler._prepared_index_name(index, include_schema=include_schema),
            compiler.preparer.format_table(index.table,
                                           use_schema=include_table_schema)
        )

        if not SchemaGenerator.minified:
            ddl += ' '

        ddl += '({});'.format(separator.join(
            compiler.sql_compiler.process(expression,
                                          include_table=False,
                                          literal_binds=True)
            for expression in index.expressions
        ))

        return ddl

    @staticmethod
    @compiles(AddConstraint)
    def __compileAddConstraint(create, compiler):
        '''Compiles ALTER TABLE ADD CONSTRAINT statements.'''
        return 'ALTER TABLE {} ADD {};'.format(
            compiler.preparer.format_table(create.element.table),
            compiler.process(create.element)
        )

    @staticmethod
    @compiles(PrimaryKeyConstraint)
    def __compilePrimaryKeyConstraint(constraint, compiler):
        '''Compiles PRIMARY KEY constraint statements.'''
        if len(constraint) == 0:
            return ''

        ddl = ''
        separator = ',' if SchemaGenerator.minified else ', '

        if constraint.name is not None:
            formatted_name = compiler.preparer.format_constraint(constraint)

            if formatted_name is not None:
                ddl += 'CONSTRAINT {} '.format(formatted_name)

        ddl += 'PRIMARY KEY'

        if not SchemaGenerator.minified:
            ddl += ' '

        ddl += '({})'.format(separator.join(
            compiler.preparer.quote(_constraint.name)
            for _constraint in (
                constraint.columns_autoinc_first \
                    if hasattr(constraint, '_implicit_generated')
                    else constraint.columns
            )
        ))
        ddl += compiler.define_constraint_deferrability(constraint)

        return ddl

    @staticmethod
    @compiles(ForeignKeyConstraint)
    def __compileForeignKeyConstraint(constraint, compiler):
        '''Compiles FOREIGN KEY constraint statements.'''
        ddl = ''
        separator = ',' if SchemaGenerator.minified else ', '

        if constraint.name is not None:
            formatted_name = compiler.preparer.format_constraint(constraint)

            if formatted_name is not None:
                ddl += 'CONSTRAINT {} '.format(formatted_name)

        remote_table = list(constraint.elements)[0].column.table

        ddl += 'FOREIGN KEY'

        if not SchemaGenerator.minified:
            ddl += ' '

        ddl += '({}) REFERENCES {}'.format(
            separator.join(
                compiler.preparer.quote(element.parent.name)
                for element in constraint.elements
            ),
            compiler.define_constraint_remote_table(constraint,
                                                    remote_table,
                                                    compiler.preparer)
        )

        if not SchemaGenerator.minified:
            ddl += ' '

        ddl += '({})'.format(separator.join(
            compiler.preparer.quote(element.column.name)
            for element in constraint.elements
        ))
        ddl += compiler.define_constraint_match(constraint)
        ddl += compiler.define_constraint_cascades(constraint)
        ddl += compiler.define_constraint_deferrability(constraint)

        return ddl

    @staticmethod
    @compiles(Insert)
    def __compileInsert(insert_stmt, compiler, **kw):
        '''Compiles INSERT statements.'''
        compiler.stack.append({
            'correlate_froms': set(),
            'asfrom_froms': set(),
            'selectable': insert_stmt,
        })
        compiler.isinsert = True
        crud_params = crud._get_crud_params(compiler, insert_stmt, **kw)

        if not crud_params:
            return

        if insert_stmt._has_multi_parameters \
                and not compiler.dialect.supports_multivalues_insert:
            return

        dml = 'INSERT INTO ' + compiler.preparer.format_table(insert_stmt.table)
        separator = ',' if SchemaGenerator.minified else ', '

        if insert_stmt.select is not None:
            dml += ' {}'.format(
                compiler.process(compiler._insert_from_select, **kw))
        elif insert_stmt._has_multi_parameters:
            dml += ' VALUES'

            if not SchemaGenerator.minified:
                dml += ' '

            dml += separator.join(
                '({})'.format(separator.join(
                    param[1] for param in crud_param_set
                ))
                for crud_param_set in crud_params
            )
        else:
            dml += ' VALUES'

            if not SchemaGenerator.minified:
                dml += ' '

            dml += '({})'.format(separator.join([
                param[1] for param in crud_params
            ]))

        compiler.stack.pop(-1)

        return dml + ';'

    # Custom DDL renderers

    def render(self, createIndexes=True):
        '''Render all SQL statements for the instance tables.

        :param createIndexes: whether or not it should create table indexes'''
        separator = '' if self.minified else '\n\n'

        return separator.join([
            self.renderCreateTable(table, createIndexes=createIndexes)
            for table in self.tables
        ])

    def renderCreateTable(self, table, createIndexes=True):
        '''Render the CREATE TABLE statement for the given table.

        :param table: the SQLAlchemy Table object to render
        :param createIndexes: whether or not it should create table indexes
        '''
        ddl = []
        separator = '' if self.minified else '\n'

        if not self.minified:
            ddl.append('--\n-- Structure for table {}\n--\n'.format(table.name))

        ddl.append(str(CreateTable(table).compile(dialect=self._dialect)))

        if len(table._data):
            ddl.append(separator + self.renderInserts(table))

        if len(table.foreign_keys) and self._dialect.supports_alter:
            ddl.append(separator + self.renderTableConstraints(table))

        if createIndexes and len(table.indexes):
            ddl.append(separator + self.renderTableIndexes(table))

        return separator.join(ddl)

    def renderInserts(self, table):
        '''Render the INSERT statements for the given table.

        :param table: the SQLAchemy Table object to render
        '''
        ddl = []
        separator = '' if self.minified else '\n'

        if not self.minified:
            ddl.append('--\n-- Data for table {}\n--\n'.format(table.name))

        for row in table._data:
            row_data = {key: str(value) for key, value in iteritems(row)}
            insert_ddl = str(table.insert().values(row_data).compile(
                compile_kwargs={'literal_binds': True},
                dialect=self._dialect,
            ))

            if self.minified and "''" in insert_ddl:
                insert_ddl = insert_ddl.replace("''", "\\'") \
                                       .replace("'", '"') \
                                       .replace('\\"', "'")

            ddl.append(insert_ddl)

        return separator.join(ddl)

    def renderTableConstraints(self, table):
        '''Render the ALTER TABLE ADD CONSTRAINT statements for the given table.

        :param table: the SQLAlchemy Table object to render
        '''
        if not self._dialect.supports_alter:
            return

        ddl = []
        separator = '' if self.minified else '\n'

        if not self.minified:
            ddl.append('--\n-- Constraints for table {}\n--\n' \
                .format(table.name))

        for constraint in table._sorted_constraints:
            if isinstance(constraint, ForeignKeyConstraint):
                ddl.append(str(
                    AddConstraint(constraint).compile(dialect=self._dialect)
                ))

        return separator.join(ddl)

    def renderTableIndexes(self, table):
        '''Render the CREATE INDEXES statements for the given table.

        :param table: the SQLAlchemy Table object to render
        '''
        ddl = []
        separator = '' if self.minified else '\n'

        if not self.minified:
            ddl.append('--\n-- Indexes for table {}\n--\n'.format(table.name))

        for index in table._sorted_indexes:
            ddl.append(str(CreateIndex(index).compile(dialect=self._dialect)))

        return separator.join(ddl)

    # Methods

    def createTable(self, entity):
        '''Add the given entity table to schema.

        :param entity: the SQLAlchemy entity object
        '''
        table = entity.__table__
        table._data = []
        table._sorted_indexes = []

        # Workaround to render table indexes in the order they were declared
        table.indexes = set()

        for column in table.columns:
            if column.index:
                table._sorted_indexes.append(Index(None,
                                                   column,
                                                   unique=bool(column.unique)))

        self.tables.append(table)

        return table

    def __str__(self):
        '''String representation of this object.'''
        return self.render()


class SqlExporter(BaseExporter):
    '''SQL exporter class.'''

    # Exporter settings
    format = 'SQL'
    extension = '.sql'
    minifiable_format = True

    def __init__(self, base, minified, dialect='default'):
        '''Constructor.

        :param base: the territorial database to export
        :param minified: whether or not the SQL statements should be minified
        :param dialect: the SQL dialect to use
        '''
        super(self.__class__, self).__init__(base, minified)

        self.schema = SchemaGenerator(dialect, self._minified)

        for entity in self._data.entities:
            data = self._data._dict[entity.__tablename__]

            if data:
                table = self.schema.createTable(entity)
                table._data = data

    @property
    def data(self):
        '''Formatted SQL representation of data.'''
        return self.schema.render()
