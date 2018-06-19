#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""SQL encoder format utils module."""
# Imports

# Built-in dependencies

from functools import reduce
from typing import Any

# External dependencies

from sqlalchemy import dialects
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.sql.schema import Column, ForeignKeyConstraint, Index, \
    PrimaryKeyConstraint, Table

# Package dependencies

from geodatabr.core.decorators import cachedmethod
from geodatabr.core.i18n import _
from geodatabr.core.types import List, OrderedMap

# Classes


class SchemaGenerator(object):
    """SQL schema generator class."""

    def __init__(self, dialect: str = 'default'):
        """
        Creates a new schema generator instance.

        Args:
            dialect: The SQL dialect to use
        """
        self._tables = List()
        self._dialect = DialectFactory(dialect)
        self._compiler = SqlCompiler(dialect)

    def addTable(self, table: Table, records: List):
        """
        Add the given table to schema.

        Args:
            table: The Table instance to add
            records: The table records list
        """
        # pylint: disable=W0212
        table._records = records

        # Workaround to render table indexes in the order they were declared
        table._sorted_indexes = List([index
                                      for column in table.columns
                                      for index in table.indexes
                                      if column in iter(index.columns)])

        self._tables.append(table)

    def render(self, create_indexes: bool = True) -> str:
        """
        Renders all SQL statements for the schema tables.

        Args:
            create_indexes: Whether or not it should create table indexes

        Returns:
            The compiled SQL statements
        """
        return '\n\n'.join([
            self.renderTable(table, create_indexes=create_indexes)
            for table in self._tables
        ])

    def renderTable(self, table: Table, create_indexes: bool = True) -> str:
        """
        Renders all SQL statements for the given table.

        Args:
            table: The Table instance to render
            create_indexes: Whether or not it should create table indexes

        Returns:
            The compiled SQL statements
        """
        # pylint: disable=W0212
        ddl = []
        ddl.append('--\n-- Structure for table "{}"\n--\n'.format(_(table.name)))
        ddl.append(self._compiler.createTable(table))

        if table._records:
            ddl.append('\n--\n-- Data for table "{}"\n--\n'.format(_(table.name)))
            ddl.append(self._compiler.inserts(table))

        if table.foreign_keys and self._dialect.supports_alter:
            ddl.append('\n--\n-- Constraints for table "{}"\n--\n'.format(_(table.name)))
            ddl.append(self._compiler.addConstraints(table))

        if create_indexes and table.indexes:
            ddl.append('\n--\n-- Indexes for table "{}"\n--\n'.format(_(table.name)))
            ddl.append(self._compiler.createIndexes(table))

        return '\n'.join(ddl)

    def __str__(self) -> str:
        """
        Returns the generated SQL.

        Returns:
            The generated SQL
        """
        return self.render()


class SqlCompiler(object):
    """Custom DDL/DML compiler."""

    def __init__(self, dialect: str = 'default'):
        """
        Creates a new SQL compiler instance.

        Args:
            dialect: The SQL dialect to use
        """
        self._dialect = DialectFactory(dialect)

    @cachedmethod()
    def _name(self, element: Any) -> str:
        """
        Gets the element name.

        Firebird dialect will be using the "p_", "f_" and "i_" prefixes for
        primary keys, foreign keys and indexes.

        Args:
            element: The element to retrieve the name

        Returns:
            The element name
        """
        if not self._dialect.name == 'firebird':
            return _(element.name)

        # Workaround for identifiers size limitation of Firebird dialect
        return reduce(lambda name, prefix: name.replace(prefix, prefix[0::2]),
                      ['pk_', 'fk_', 'ix_'],
                      _(element.name))

    @cachedmethod()
    def createTable(self, table: Table) -> str:
        """
        Compiles a CREATE TABLE statement for a given table.

        Args:
            table: The Table instance to compile

        Returns:
            str: The DDL for the CREATE TABLE statement
        """
        # pylint: disable=W0212
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
    def createColumn(self, column: Column) -> str:
        """
        Compiles a given column element for use in CREATE TABLE statement.

        Args:
            column: The Column instance to compile

        Returns:
            The DDL for the column element
        """
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
    def createColumns(self, table: Table) -> str:
        """
        Compiles a given table columns elements for use in CREATE TABLE
        statement.

        Args:
            table: The Table instance to compile

        Returns:
            The DDL for the table columns elements
        """
        separator = '\n'
        ddl = ''

        for column in table.columns:
            column_ddl = self.createColumn(column)

            if column_ddl is not None:
                ddl += separator + '  ' + column_ddl
                separator = ',\n'

        return ddl

    @cachedmethod()
    def createConstraints(self, table: Table) -> str:
        """
        Compiles a given table constraints for use in CREATE TABLE statement.

        Args:
            table: The Table instance to compile

        Returns:
            The DDL for the table constraints elements
        """
        return ',\n  '.join(
            self.constraint(constraint)
            for constraint in table.constraints
            if not hasattr(constraint, 'use_alter') or not constraint.use_alter)

    @cachedmethod()
    def createIndex(self, index: Index) -> str:
        """
        Compiles a CREATE INDEX statement for a given index.

        Args:
            index: The Index instance to compile

        Returns:
            The DDL for the CREATE INDEX statement
        """
        ddl = 'CREATE '

        if index.unique:
            ddl += 'UNIQUE '

        ddl += 'INDEX {} ON {} ({});'.format(
            self._name(index),
            _(index.table.name),
            ', '.join(_(column.name) for column in index.expressions))

        return ddl

    @cachedmethod()
    def createIndexes(self, table: Table) -> str:
        """
        Compiles the CREATE INDEX statements for a given table.

        Args:
            table: The Table instance to compile

        Returns:
            The DDL for the CREATE INDEX statements
        """
        # pylint: disable=W0212
        return '\n'.join(self.createIndex(index)
                         for index in table._sorted_indexes)

    @cachedmethod()
    def constraint(self, constraint: Any) -> str:
        """
        Compiles a given constraint element for use in CREATE TABLE
        and ALTER TABLE statements.

        Args:
            constraint: The constraint instance to compile

        Returns:
            The DDL for the constraint element
        """
        if isinstance(constraint, PrimaryKeyConstraint):
            return self.primaryKeyConstraint(constraint)

        if isinstance(constraint, ForeignKeyConstraint):
            return self.foreignKeyConstraint(constraint)

        return ''

    @cachedmethod()
    def primaryKeyConstraint(self, constraint: PrimaryKeyConstraint) -> str:
        """
        Compiles a given primary key constraint element for use in CREATE TABLE
        and ALTER TABLE statements.

        Args:
            constraint: The PrimaryKeyConstraint instance to compile

        Returns:
            The DDL for the primary key constraint element
        """
        ddl = ''

        if constraint.name is not None:
            ddl += 'CONSTRAINT {} '.format(self._name(constraint))

        ddl += 'PRIMARY KEY ({})'.format(
            ', '.join(_(column.name) for column in constraint.columns))

        return ddl

    @cachedmethod()
    def foreignKeyConstraint(self, constraint: ForeignKeyConstraint) -> str:
        """
        Compiles a given foreign key constraint element for use in CREATE TABLE
        and ALTER TABLE statements.

        Args:
            constraint: The ForeignKeyConstraint instance to compile

        Returns:
            The DDL for the foreign key constraint element
        """
        ddl = ''

        if constraint.name is not None:
            ddl += 'CONSTRAINT {} '.format(self._name(constraint))

        remote_table = list(constraint.elements)[0].column.table

        ddl += 'FOREIGN KEY ({}) REFERENCES {} ({})'.format(
            ', '.join(_(element.parent.name)
                      for element in constraint.elements),
            _(remote_table.name),
            ', '.join(_(element.column.name)
                      for element in constraint.elements))

        return ddl

    @cachedmethod()
    def addConstraint(self, constraint: Any) -> str:
        """
        Compiles a ALTER TABLE ADD CONSTRAINT statement for a given constraint.

        Args:
            constraint: The constraint instance to compile

        Returns:
            The DDL for the ALTER TABLE ADD CONSTRAINT statement
        """
        if not self._dialect.supports_alter:
            return ''

        return 'ALTER TABLE {} ADD {};'.format(_(constraint.table.name),
                                               self.constraint(constraint))

    @cachedmethod()
    def addConstraints(self, table: Table) -> str:
        """
        Compiles the ALTER TABLE ADD CONSTRAINT statements for a given table.

        Args:
            table: The Table instance to compile

        Returns:
            The DDL for the ALTER TABLE ADD CONSTRAINT statements
        """
        # pylint: disable=W0212
        if not self._dialect.supports_alter:
            return ''

        ddl = []

        for constraint in table._sorted_constraints:
            # if self.dialect.supports_alter or getattr(constraint, 'use_alter', False)
            if isinstance(constraint, ForeignKeyConstraint):
                ddl.append(self.addConstraint(constraint))

        return '\n'.join(ddl)

    def insert(self, table: Table, record: OrderedMap) -> str:
        """
        Compiles a INSERT statement for a given table and record.

        Args:
            table: The Table instance to compile
            record: The table record mapping

        Returns:
            The DML for the INSERT statements
        """
        def _compile_literals(record):
            return ', '.join(
                table.columns.get(column).type.literal_processor(
                    dialect=self._dialect)(value)
                for column, value in record.items())

        dml = 'INSERT INTO ' + _(table.name)

        if any(isinstance(record, _type) for _type in (list, set, tuple)) \
                and self._dialect.supports_multivalues_insert:
            dml += ' VALUES {};'.format(
                ', '.join('({})'.format(_compile_literals(_record))
                          for _record in record))
        else:
            dml += ' VALUES ({});'.format(_compile_literals(record))

        return dml

    @cachedmethod()
    def inserts(self, table: Table) -> str:
        """
        Compiles the INSERT statements for a given table and list of records.

        Args:
            table: The Table instance to compile

        Returns:
            The DML for the INSERT statements
        """
        # pylint: disable=W0212
        return '\n'.join(self.insert(table, record)
                         for record in table._records)


class DialectFactory(object):
    """Factory class for instantiation of SQL dialect implementations."""

    def __new__(cls, dialect: str) -> Dialect:
        """
        Gets the given SQL dialect instance by name.

        Args:
            dialect: The SQL dialect name

        Returns:
            The SQL dialect instance
        """
        if dialect == 'default':
            return DefaultDialect()

        if dialect in ['firebird', 'mssql', 'mysql', 'oracle', 'postgresql',
                       'sqlite', 'sybase']:
            return dialects.registry.load(dialect)()

        raise UnsupportedDialectError('Unsupported dialect: {}'.format(dialect))


class UnsupportedDialectError(Exception):
    """Exception class raised when a given SQL dialect is not supported."""
    pass
