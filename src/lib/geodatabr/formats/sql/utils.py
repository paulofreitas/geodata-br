#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
SQL file format utils module
'''
# Imports

# External dependencies

from sqlalchemy import dialects
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.sql.schema import ForeignKeyConstraint, PrimaryKeyConstraint

# Package dependencies

from geodatabr.core.helpers.decorators import cachedmethod
from geodatabr.core.i18n import _, Translator

# Translator setup

Translator.load('dataset')

# Classes


class SchemaGenerator(object):
    '''
    SQL schema generator class.
    '''

    def __init__(self, dialect='default'):
        '''
        Constructor.

        Arguments:
            dialect (str): The SQL dialect to use
        '''
        self._tables = []
        self._dialect = DialectFactory(dialect)
        self._compiler = SqlCompiler(dialect)

    def addTable(self, table, records):
        '''
        Add the given table to schema.

        Arguments:
            table (sqlalchemy.sql.schema.Table): The Table instance to add
            records (geodatabr.core.types.OrderedMap): The table records mapping
        '''
        table._records = records

        # Workaround to render table indexes in the order they were declared
        table._sorted_indexes = [index
                                 for column in table.columns
                                 for index in table.indexes
                                 if column in iter(index.columns)]

        self._tables.append(table)

    def render(self, createIndexes=True):
        '''
        Render all SQL statements for the schema tables.

        Arguments:
            createIndexes (bool): Whether or not it should create table indexes

        Returns:
            str: The compiled SQL statements
        '''
        return '\n\n'.join([
            self.renderTable(table, createIndexes=createIndexes)
            for table in self._tables
        ])

    def renderTable(self, table, createIndexes=True):
        '''
        Render all SQL statements for the given table.

        Arguments:
            table (sqlalchemy.sql.schema.Table): The Table instance to render
            createIndexes (bool): Whether or not it should create table indexes

        Returns:
            str: The compiled SQL statements
        '''
        ddl = []
        ddl.append('--\n-- Structure for table "{}"\n--\n'.format(_(table.name)))
        ddl.append(self._compiler.createTable(table))

        if len(table._records):
            ddl.append('\n--\n-- Data for table "{}"\n--\n'.format(_(table.name)))
            ddl.append(self._compiler.inserts(table, table._records.values()))

        if len(table.foreign_keys) and self._dialect.supports_alter:
            ddl.append('\n--\n-- Constraints for table "{}"\n--\n'.format(_(table.name)))
            ddl.append(self._compiler.addConstraints(table))

        if createIndexes and len(table.indexes):
            ddl.append('\n--\n-- Indexes for table "{}"\n--\n'.format(_(table.name)))
            ddl.append(self._compiler.createIndexes(table))

        return '\n'.join(ddl)

    def __str_(self):
        '''
        Return the generated SQL.

        Returns:
            str: The generated SQL
        '''
        return self.render()


class SqlCompiler(object):
    '''
    Custom DDL/DML compiler.
    '''

    def __init__(self, dialect='default'):
        '''
        Constructor.

        Arguments:
            dialect (str): The SQL dialect to use
        '''
        self._dialect = DialectFactory(dialect)

    @cachedmethod()
    def createTable(self, table):
        '''
        Compile a CREATE TABLE statement for a given table.

        Args:
            table (sqlalchemy.sql.schema.Table): The Table instance to compile

        Returns:
            str: The DDL for the CREATE TABLE statement
        '''
        ddl = 'CREATE '

        if table._prefixes:
            ddl += ' '.join(table._prefixes) + ' '

        ddl += 'TABLE {} ('.format(_(table.name))
        ddl += self.createColumns(table)

        constraints_ddl = self.createConstraints(table)

        if constraints_ddl:
            ddl += ',\n  ' + constraints_ddl

        ddl += '\n);'

        return ddl

    @cachedmethod()
    def createColumn(self, column):
        '''
        Compile a given column element for use in CREATE TABLE statement.

        Args:
            column (sqlalchemy.sql.schema.Column):
                The Column instance to compile

        Returns:
            str: The DDL for the column element
        '''
        ddl = '{} {}'.format(_(column.name), column.type)

        if column.default is not None:
            ddl += ' DEFAULT ' + column.default

        if not column.nullable:
            ddl += ' NOT NULL'

        if column.constraints:
            ddl += ' '.join(self.constraint(constraint)
                            for constraint in column.constraints)

        return ddl

    @cachedmethod()
    def createColumns(self, table):
        '''
        Compile a given table columns elements for use in CREATE TABLE statement.

        Args:
            table (sqlalchemy.sql.schema.Table): The Table instance to compile

        Returns:
            str: The DDL for the table columns elements
        '''
        separator = '\n'
        ddl = ''

        for column in table.columns:
            column_ddl = self.createColumn(column)

            if column_ddl is not None:
                ddl += separator + '  ' + column_ddl
                separator = ',\n'

        return ddl

    @cachedmethod()
    def createConstraints(self, table):
        '''
        Compile a given table constraints for use in CREATE TABLE statement.

        Args:
            table (sqlalchemy.sql.schema.Table): The Table instance to compile

        Returns:
            str: The DDL for the table constraints elements
        '''
        return ',\n  '.join(
            self.constraint(constraint)
            for constraint in table.constraints
            if not hasattr(constraint, 'use_alter') or not constraint.use_alter)

    @cachedmethod()
    def createIndex(self, index):
        '''
        Compile a CREATE INDEX statement for a given index.

        Args:
            index (sqlalchemy.sql.schema.Index): The Index instance to compile

        Returns:
            str: The DDL for the CREATE INDEX statement
        '''
        ddl = 'CREATE '

        if index.unique:
            ddl += 'UNIQUE '

        ddl += 'INDEX {} ON {} ({});'.format(
            _(index.name),
            _(index.table.name),
            ', '.join(_(column.name) for column in index.expressions))

        return ddl

    @cachedmethod()
    def createIndexes(self, table):
        '''
        Compile the CREATE INDEX statements for a given table.

        Args:
            table (sqlalchemy.sql.schema.Table): The Table instance to compile

        Returns:
            str: The DDL for the CREATE INDEX statements
        '''
        return '\n'.join(self.createIndex(index)
                         for index in table._sorted_indexes)

    @cachedmethod()
    def constraint(self, constraint):
        '''
        Compile a given constraint element for use in CREATE TABLE
        and ALTER TABLE statements.

        Args:
            constraint: The constraint instance to compile

        Returns:
            str: The DDL for the constraint element
        '''
        if isinstance(constraint, PrimaryKeyConstraint):
            return self.primaryKeyConstraint(constraint)

        if isinstance(constraint, ForeignKeyConstraint):
            return self.foreignKeyConstraint(constraint)

    @cachedmethod()
    def primaryKeyConstraint(self, constraint):
        '''
        Compile a given primary key constraint element for use in CREATE TABLE
        and ALTER TABLE statements.

        Args:
            constraint (sqlalchemy.sql.schema.PrimaryKeyConstraint):
                The PrimaryKeyConstraint instance to compile

        Returns:
            str: The DDL for the primary key constraint element
        '''
        ddl = ''

        if constraint.name is not None:
            ddl += 'CONSTRAINT {} '.format(_(constraint.name))

        ddl += 'PRIMARY KEY ({})'.format(
            ', '.join(_(_constraint.name)
                      for _constraint in constraint.columns))

        return ddl

    @cachedmethod()
    def foreignKeyConstraint(self, constraint):
        '''
        Compile a given foreign key constraint element for use in CREATE TABLE
        and ALTER TABLE statements.

        Args:
            constraint (sqlalchemy.sql.schema.ForeignKeyConstraint):
                The ForeignKeyConstraint instance to compile

        Returns:
            str: The DDL for the foreign key constraint element
        '''
        ddl = ''

        if constraint.name is not None:
            ddl += 'CONSTRAINT {} '.format(_(constraint.name))

        remote_table = list(constraint.elements)[0].column.table

        ddl += 'FOREIGN KEY ({}) REFERENCES {} ({})'.format(
            ', '.join(_(element.parent.name)
                      for element in constraint.elements),
            _(remote_table.name),
            ', '.join(_(element.column.name)
                      for element in constraint.elements))

        return ddl

    @cachedmethod()
    def addConstraint(self, constraint):
        '''
        Compile a ALTER TABLE ADD CONSTRAINT statement for a given constraint.

        Args:
            constraint: The constraint instance to compile

        Returns:
            str: The DDL for the ALTER TABLE ADD CONSTRAINT statement
        '''
        return 'ALTER TABLE {} ADD {};'.format(_(constraint.table.name),
                                               self.constraint(constraint))

    @cachedmethod()
    def addConstraints(self, table):
        '''
        Compile the ALTER TABLE ADD CONSTRAINT statements for a given table.

        Args:
            table (sqlalchemy.sql.schema.Table): The Table instance to compile

        Returns:
            str: The DDL for the ALTER TABLE ADD CONSTRAINT statements
        '''
        if not self._dialect.supports_alter:
            return

        ddl = []

        for constraint in table._sorted_constraints:
            # if self.dialect.supports_alter or getattr(constraint, 'use_alter', False)
            if isinstance(constraint, ForeignKeyConstraint):
                ddl.append(self.addConstraint(constraint))

        return '\n'.join(ddl)

    def insert(self, table, record):
        '''
        Compile a INSERT statement for a given table and record.

        Args:
            table (sqlalchemy.sql.schema.Table): The Table instance to compile
            record (geodatabr.core.types.OrderedMap): The table record mapping

        Returns:
            str: The DML for the INSERT statements
        '''
        def _compileLiterals(record):
            return ', '.join(
                table.columns.get(column).type \
                    .literal_processor(dialect=self._dialect)(value)
                for column, value in record.items())

        dml = 'INSERT INTO ' + _(table.name)

        if any(isinstance(record, _type) for _type in (list, set, tuple)) \
                and self._dialect.supports_multivalues_insert:
            dml += ' VALUES {};'.format(
                ', '.join('({})'.format(_compileLiterals(_record))
                          for _record in record))
        else:
            dml += ' VALUES ({});'.format(_compileLiterals(record))

        return dml

    @cachedmethod()
    def inserts(self, table, records):
        '''
        Compile the INSERT statements for a given table and list of records.

        Args:
            table (sqlalchemy.sql.schema.Table): The Table instance to compile
            records (list): The list of table records

        Returns:
            str: The DML for the INSERT statements
        '''
        return '\n'.join(self.insert(table, record) for record in records)


class DialectFactory(object):
    '''
    Factory class for instantiation of SQL dialect implementations.
    '''

    def __new__(cls, dialect):
        '''
        Get the given SQL dialect instance by name.

        Arguments:
            dialect (str): The SQL dialect name

        Returns:
            type: The SQL dialect instance
        '''
        if dialect == 'default':
            return DefaultDialect()

        if dialect in ['firebird', 'mssql', 'mysql', 'oracle', 'postgresql',
                       'sqlite', 'sybase']:
            return dialects.registry.load(dialect)()

        raise UnsupportedDialectError('Unsupported dialect: {}'.format(dialect))


class UnsupportedDialectError(Exception):
    '''
    Exception class raised when a given SQL dialect is not supported.
    '''
    pass
