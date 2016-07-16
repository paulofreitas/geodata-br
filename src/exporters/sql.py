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

# -- Imports ------------------------------------------------------------------

# Built-in modules

import collections

# Dependency modules
from builtins import str
from sqlalchemy.dialects import firebird, mssql, mysql, oracle, postgresql, sqlite, sybase
from sqlalchemy.engine import default
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import crud
from sqlalchemy.sql.ddl import AddConstraint, CreateColumn, CreateIndex, CreateTable
from sqlalchemy.sql.dml import Insert
from sqlalchemy.sql.schema import Column, Constraint, ForeignKey, ForeignKeyConstraint, Index, MetaData, PrimaryKeyConstraint, Table
from sqlalchemy.types import BigInteger, Integer, SmallInteger, String

# Package modules

from .base import BaseExporter

# -- Implementation -----------------------------------------------------------


class SchemaGenerator(object):
    convention = {
      'pk': 'pk_%(table_name)s',
      'fk': 'fk_%(table_name)s_%(column_0_name)s',
      'ix': 'ix_%(column_0_label)s',
      'uq': 'uq_%(table_name)s_%(column_0_name)s',
    }

    minified = False

    def __init__(self, dialect='default', minified=False):
        self.metadata = MetaData(naming_convention=self.convention)
        self.tables = []
        self.dialect = dialect
        self._dialect = self.getDialect(dialect)

        SchemaGenerator.minified = minified

    def getDialect(self, dialect):
        if dialect == 'default':
            return default.DefaultDialect()

        if dialect in ['firebird', 'mssql', 'mysql', 'oracle', 'postgresql',
                       'sqlite', 'sybase']:
            return globals()[dialect].dialect()

        raise Exception('Unsupported dialect: {}'.format(dialect))

    # Custom DDL/DML compilers

    @compiles(CreateColumn)
    def __compileCreateColumn(create, compiler, **kw):
        column = create.element

        ddl = '{} {}'.format(column.name,
                             compiler.type_compiler.process(column.type))

        default = compiler.get_column_default_string(column)

        if default is not None:
            ddl += ' DEFAULT ' + default

        if not column.nullable:
            ddl += ' NOT NULL'

        if column.constraints:
            ddl += ' '.join(compiler.process(constraint)
                            for constraint in column.constraints)

        return ddl

    @compiles(CreateTable)
    def __compileCreateTable(create, compiler, **kw):
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
            except:
                pass

        constraints_ddl = compiler.create_table_constraints(
            table
            #_include_foreign_key_constraints=True #create.include_foreign_key_constraints
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

    @compiles(CreateIndex)
    def __compileCreateIndex(create,
                             compiler,
                             include_schema=False,
                             include_table_schema=True):
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

    @compiles(AddConstraint)
    def __compileAddConstraint(create, compiler):
        return 'ALTER TABLE {} ADD {};'.format(
            compiler.preparer.format_table(create.element.table),
            compiler.process(create.element)
        )

    @compiles(PrimaryKeyConstraint)
    def __compilePrimaryKeyConstraint(constraint, compiler):
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

    @compiles(ForeignKeyConstraint)
    def __compileForeignKeyConstraint(constraint, compiler):
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

    @compiles(Insert)
    def __compileInsert(insert_stmt, compiler, **kw):
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

    def createTable(self, table_name, properties):
        table = Table(table_name, self.metadata)
        table._data = []
        table._constraints = []
        table._indexes = []

        # Workarounds to render table properties in the order they were declared
        for table_property in properties:
            if isinstance(table_property, Column):
                column = table_property

                table.append_column(column)

                if column.index:
                    table._indexes.append(Index(None,
                                                column,
                                                unique=bool(column.unique)))

                for foreign_key in column.foreign_keys:
                    table._constraints.append(foreign_key.constraint)
            elif isinstance(table_property, Index):
                index = table_property

                table.append_constraint(index)
                table._indexes.append(index)
            elif isinstance(table_property, Constraint):
                constraint = table_property

                table.append_constraint(constraint)

                if isinstance(constraint, ForeignKeyConstraint):
                    table._constraints.append(constraint)

        self.tables.append(table)

    def render(self, createIndexes=True):
        separator = '' if self.minified else '\n\n'

        return separator.join([
            self.renderCreateTable(table, createIndexes=createIndexes)
            for table in self.tables
        ])

    def renderCreateTable(self, table, createIndexes=True):
        ddl = []
        include_foreign_keys = None
        separator = '' if self.minified else '\n'

        if not self.minified:
            ddl.append('--\n-- Structure for table {}\n--\n'.format(table.name))

        if not self._dialect.supports_alter:
            include_foreign_keys = True

        ddl.append(str(
            CreateTable(table,
                        include_foreign_key_constraints=include_foreign_keys) \
                .compile(dialect=self._dialect)
        ))

        if len(table._data):
            ddl.append(separator + self.renderInserts(table))

        if len(table._constraints) and self._dialect.supports_alter:
            ddl.append(separator + self.renderTableConstraints(table))

        if createIndexes and len(table._indexes):
            ddl.append(separator + self.renderTableIndexes(table))

        return separator.join(ddl)

    def renderInserts(self, table):
        ddl = []
        separator = '' if self.minified else '\n'

        if not self.minified:
            ddl.append('--\n-- Dumping data for table {}\n--\n' \
                .format(table.name))

        for row in table._data:
            insert_ddl = str(table.insert().values(row).compile(
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
        if not self._dialect.supports_alter:
            return

        ddl = []
        separator = '' if self.minified else '\n'

        if not self.minified:
            ddl.append('--\n-- Constraints for table {}\n--\n' \
                .format(table.name))

        for constraint in table._constraints:
            ddl.append(str(
                AddConstraint(constraint).compile(dialect=self._dialect)
            ))

        return separator.join(ddl)

    def renderTableIndexes(self, table):
        ddl = []
        separator = '' if self.minified else '\n'

        if not self.minified:
            ddl.append('--\n-- Indexes for table {}\n--\n'.format(table.name))

        for index in table._indexes:
            ddl.append(str(CreateIndex(index).compile(dialect=self._dialect)))

        return separator.join(ddl)

    def __str__(self):
        return self.render()


class SqlExporter(BaseExporter):
    '''SQL exporter class.'''
    format = 'SQL'
    extension = '.sql'

    def __init__(self, base, minified, dialect='default'):
        super(self.__class__, self).__init__(base, minified)

        self.dialect = dialect

        self._buildSchema()

    def _buildSchema(self):
        self.schema = SchemaGenerator(self.dialect, self._minified)
        self.schema.createTable('uf', [
            Column('id',
                   SmallInteger,
                   nullable=False,
                   primary_key=True),
            Column('nome',
                   String(32),
                   nullable=False,
                   index=True),
        ]),
        self.schema.createTable('mesorregiao', [
            Column('id',
                   SmallInteger,
                   nullable=False,
                   primary_key=True),
            Column('id_uf',
                   SmallInteger,
                   ForeignKey('uf.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('nome',
                   String(64),
                   nullable=False,
                   index=True),
        ]),
        self.schema.createTable('microrregiao', [
            Column('id',
                   Integer,
                   nullable=False,
                   primary_key=True),
            Column('id_mesorregiao',
                   SmallInteger,
                   ForeignKey('mesorregiao.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('id_uf',
                   SmallInteger,
                   ForeignKey('uf.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('nome',
                   String(64),
                   nullable=False,
                   index=True),
        ]),
        self.schema.createTable('municipio', [
            Column('id',
                   Integer,
                   nullable=False,
                   primary_key=True),
            Column('id_microrregiao',
                   Integer,
                   ForeignKey('microrregiao.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('id_mesorregiao',
                   SmallInteger,
                   ForeignKey('mesorregiao.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('id_uf',
                   SmallInteger,
                   ForeignKey('uf.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('nome',
                   String(64),
                   nullable=False,
                   index=True),
        ]),
        self.schema.createTable('distrito', [
            Column('id',
                   Integer,
                   nullable=False,
                   primary_key=True),
            Column('id_municipio',
                   Integer,
                   ForeignKey('municipio.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('id_microrregiao',
                   Integer,
                   ForeignKey('microrregiao.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('id_mesorregiao',
                   SmallInteger,
                   ForeignKey('mesorregiao.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('id_uf',
                   SmallInteger,
                   ForeignKey('uf.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('nome',
                   String(64),
                   nullable=False,
                   index=True),
        ]),
        self.schema.createTable('subdistrito', [
            Column('id',
                   BigInteger,
                   nullable=False,
                   primary_key=True),
            Column('id_distrito',
                   Integer,
                   ForeignKey('distrito.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('id_municipio',
                   Integer,
                   ForeignKey('municipio.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('id_microrregiao',
                   Integer,
                   ForeignKey('microrregiao.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('id_mesorregiao',
                   SmallInteger,
                   ForeignKey('mesorregiao.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('id_uf',
                   SmallInteger,
                   ForeignKey('uf.id', use_alter=True),
                   nullable=False,
                   index=True),
            Column('nome',
                   String(64),
                   nullable=False,
                   index=True),
        ])

        # Insert data into tables
        for table in self.schema.tables:
            table._data = self._data._dict[table.name]

    def __str__(self):
        return self.schema.render()
