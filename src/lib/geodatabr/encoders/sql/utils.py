#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""SQL encoder format utils module."""
# Imports

# Built-in dependencies

from typing import Any

# External dependencies

from sqlalchemy import dialects
from sqlalchemy.engine import default, interfaces
from sqlalchemy.sql import schema

# Package dependencies

from geodatabr.core import decorators, i18n, types

# Classes


class Compiler(types.AbstractClass):
    """
    Abstract SQL compiler class.

    Attributes:
        dialect (sqlalchemy.engine.interfaces.Dialect): The SQL dialect
        naming_convention (dict): The SQL naming convention
    """

    def __init__(self, dialect: str = None):
        """
        Creates a new SQL compiler instance.

        Args:
            dialect: The SQL dialect name to use
        """
        self.dialect = Dialect.factory(dialect or 'default')
        self.naming_convention = Dialect.getNamingConvention(self.dialect)

    def compile(self) -> str:
        """
        Abstract method used to compile SQL statements.

        Returns:
            The compiled SQL statements
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """
        Returns the compiled SQL statements.

        Returns:
            The compiled SQL statements
        """
        return self.compile()


class Column(Compiler):
    """SQL compiler class used to compile table columns."""

    def __init__(self, column: schema.Column, dialect: str = None):
        """
        Creates a new table column compiler instance.

        Args:
            column: The table column element to compile
            dialect: The SQL dialect name to use
        """
        self.column = column

        super().__init__(dialect)

    @decorators.cachedmethod()
    def compile(self) -> str:
        """
        Compiles the DDL statement for the table column element.

        Returns:
            The compiled DDL statement for the table column element
        """
        ddl = '{name} {type}'.format(name=i18n._(self.column.name),
                                     type=self.column.type)

        if self.column.default is not None:
            ddl += ' DEFAULT ' + self.column.default

        if not self.column.nullable:
            ddl += ' NOT NULL'

        if self.column.constraints:
            ddl += ' '.join(str(Constraint(constraint,
                                           dialect=self.dialect.name))
                            for constraint in self.column.constraints)

        return ddl


class ColumnCollection(Compiler):
    """SQL compiler class used to compile the columns of a given table."""

    def __init__(self, table: schema.Table, dialect: str = None):
        """
        Creates a new table column collection compiler instance.

        Args:
            table: The table element to compile
            dialect: The SQL dialect name to use
        """
        self.table = table

        super().__init__(dialect)

    @decorators.cachedmethod()
    def compile(self) -> str:
        """
        Compiles the DDL statements for the table columns.

        Returns:
            The compiled DDL statements for the table columns
        """
        return ',\n'.join('  ' + str(Column(column,
                                            dialect=self.dialect.name))
                          for column in self.table.columns)


class Constraint(Compiler):
    """SQL compiler class used to compile table constraints."""

    def __init__(self, constraint: Any, dialect: str = None):
        """
        Creates a new table constraint compiler instance.

        Args:
            constraint: The table constraint element to compile
            dialect: The SQL dialect name to use
        """
        self.constraint = constraint

        super().__init__(dialect)

    def _compilePrimaryKey(self) -> str:
        """
        Compiles the DDL statement for a table primary key element.

        Returns:
            The compiled DDL statement for the table primary key element
        """
        ddl = ''

        if self.constraint.name is not None:
            ddl += 'CONSTRAINT {name} '.format(
                name=self.naming_convention[type(self.constraint)]) \
                .format(table_name=i18n._(self.constraint.table.name))

        return ddl + 'PRIMARY KEY ({columns})'.format(
            columns=', '.join(i18n._(column.name)
                              for column in self.constraint.columns))

    def _compileForeignKey(self) -> str:
        """
        Compiles the DDL statement for a table foreign key element.

        Returns:
            The compiled DDL statement for the table foreign key element
        """
        ddl = ''

        if self.constraint.name is not None:
            ddl += 'CONSTRAINT {name} '.format(
                name=self.naming_convention[type(self.constraint)]) \
                .format(table_name=i18n._(self.constraint.table.name),
                        column_name=i18n._(self.constraint.column_keys[0]))

        ddl += 'FOREIGN KEY ({columns}) REFERENCES {ref_table} ({ref_columns})'

        return ddl.format(
            columns=', '.join(i18n._(element.parent.name)
                              for element in self.constraint.elements),
            ref_table=i18n._(list(
                self.constraint.elements)[0].column.table.name),
            ref_columns=', '.join(i18n._(element.column.name)
                                  for element in self.constraint.elements))

    @decorators.cachedmethod()
    def compile(self) -> str:
        """
        Compiles the DDL statement for the table constraint element.

        Returns:
            The compiled DDL statement for the table constraint element
        """
        ddl = ''

        if isinstance(self.constraint, schema.PrimaryKeyConstraint):
            ddl += self._compilePrimaryKey()

        if isinstance(self.constraint, schema.ForeignKeyConstraint):
            ddl += self._compileForeignKey()

        if (not getattr(self.constraint, 'use_alter', False)
                or not self.dialect.supports_alter):
            return ddl

        return 'ALTER TABLE {table} ADD {constraint};'.format(
            table=i18n._(self.constraint.table.name),
            constraint=ddl)


class ConstraintCollection(Compiler):
    """SQL compiler class used to compile the constraints of a given table."""

    def __init__(self,
                 table: schema.Table,
                 use_alter: bool = False,
                 dialect: str = None):
        """
        Creates a new table constraint collection compiler instance.

        Args:
            table: The table element to compile
            use_alter: If it should compile foreign keys out-of-line
            dialect: The SQL dialect name to use
        """
        self.table = table
        self.use_alter = use_alter

        super().__init__(dialect)

    @decorators.cachedmethod()
    def compile(self) -> str:
        """
        Compiles the DDL statements for the table constraints.

        Returns:
            The compiled DDL statements for the table constraints
        """
        # pylint: disable=protected-access
        if not self.use_alter:
            return ',\n  '.join(
                str(Constraint(constraint, dialect=self.dialect.name))
                for constraint in self.table._sorted_constraints
                if (not getattr(constraint, 'use_alter', False)
                    or not self.dialect.supports_alter))

        if not self.table.foreign_keys or not self.dialect.supports_alter:
            return ''

        ddl = '\n\n--\n-- Constraints for table "{table}"\n--\n\n{constraints}'

        return ddl.format(
            table=i18n._(self.table.name),
            constraints='\n'.join(
                str(Constraint(constraint, dialect=self.dialect.name))
                for constraint in self.table._sorted_constraints
                if (isinstance(constraint, schema.ForeignKeyConstraint)
                    and getattr(constraint, 'use_alter', False))))


class Index(Compiler):
    """SQL compiler class used to compile table indexes."""

    def __init__(self, index: schema.Index, dialect: str = None):
        """
        Creates a new table index compiler instance.

        Args:
            index: The table index element to compile
            dialect: The SQL dialect name to use
        """
        self.index = index

        super().__init__(dialect)

    @decorators.cachedmethod()
    def compile(self) -> str:
        """
        Compiles the DDL statement for the table index element.

        Returns:
            The compiled DDL statement for the table index element
        """
        # pylint: disable=protected-access
        ddl = 'CREATE '

        if self.index.unique:
            ddl += 'UNIQUE '

        ddl += 'INDEX {name} ON {table_name} ({column_names});'

        return ddl.format(name=self.naming_convention[type(self.index)],
                          table_name=i18n._(self.index.table.name),
                          column_names=', '.join(
                              i18n._(column.name)
                              for column in self.index.expressions)) \
                  .format(table_name=i18n._(self.index.table.name),
                          column_name=i18n._(self.index.expressions[0].name))


class IndexCollection(Compiler):
    """SQL compiler class used to compile the indexes of a given table."""

    def __init__(self, table: schema.Table, dialect: str = None):
        """
        Creates a new table index collection compiler instance.

        Args:
            table: The table element to compile
            dialect: The SQL dialect name to use
        """
        self.table = table

        super().__init__(dialect)

    @decorators.cachedmethod()
    def compile(self) -> str:
        """
        Compiles the DDL statements for the table indexes.

        Returns:
            The compiled DDL statements for the table indexes
        """
        # pylint: disable=protected-access
        if not self.table.indexes:
            return ''

        return '\n\n--\n-- Indexes for table "{table}"\n--\n\n{indexes}' \
            .format(table=i18n._(self.table.name),
                    indexes='\n'.join(
                        str(Index(index, dialect=self.dialect.name))
                        for index in self.table._sorted_indexes))


class Row(Compiler):
    """SQL compiler class used to compile table rows."""

    def __init__(self,
                 table: schema.Table,
                 row: types.OrderedMap,
                 dialect: str = None):
        """
        Creates a new table row compiler instance.

        Args:
            table: The table element to compile
            row: The table row mapping
            dialect: The SQL dialect name to use
        """
        self.table = table
        self.row = row

        super().__init__(dialect)

    @decorators.cachedmethod()
    def compile(self) -> str:
        """
        Compiles the DML statement for the table row.

        Returns:
            The compiled DML statement for the table row
        """
        def _compile_literals(row):
            return ', '.join(
                self.table.columns.get(column).type.literal_processor(
                    dialect=self.dialect)(value)
                for column, value in row.items())

        if (any(isinstance(self.row, _type) for _type in (list, set, tuple))
                and self.dialect.supports_multivalues_insert):
            return 'INSERT INTO {table} VALUES {values};'.format(
                table=i18n._(self.table.name),
                values=', '.join('({})'.format(_compile_literals(row))
                                 for row in self.row))

        return 'INSERT INTO {table} VALUES ({values});'.format(
            table=i18n._(self.table.name),
            values=_compile_literals(self.row))


class RowCollection(Compiler):
    """SQL compiler class used to compile the rows of a given table."""

    def __init__(self, table: schema.Table, dialect: str = None):
        """
        Creates a new table row collection compiler instance.

        Args:
            table: The table element to compile
            dialect: The SQL dialect name to use
        """
        self.table = table

        super().__init__(dialect)

    @decorators.cachedmethod()
    def compile(self) -> str:
        """
        Compiles the DML statements for the table rows.

        Returns:
            The compiled DML statements for the table rows
        """
        if not self.table.rows:
            return ''

        return '\n\n--\n-- Data for table "{table}"\n--\n\n{rows}'.format(
            table=i18n._(self.table.name),
            rows='\n'.join(str(Row(self.table,
                                   row,
                                   dialect=self.dialect.name))
                           for row in self.table.rows))


class Table(Compiler):
    """SQL compiler class used to compile tables."""

    def __init__(self, table: schema.Table, dialect: str = None):
        """
        Creates a new table compiler instance.

        Args:
            table: The table element to compile
            dialect: The SQL dialect name to use
        """
        self.table = table

        super().__init__(dialect)

    @decorators.cachedmethod()
    def compile(self) -> str:
        """
        Compiles the DDL/DML statements for the table.

        Returns:
            The compiled DDL/DML statements for the table
        """
        ddl = '--\n-- Structure for table "{table}"\n--\n\n' \
              'CREATE TABLE {table} (\n{columns}' \
              .format(table=i18n._(self.table.name),
                      columns=ColumnCollection(self.table,
                                               dialect=self.dialect.name))

        if self.table.constraints:
            ddl += ',\n  ' + str(ConstraintCollection(
                self.table,
                dialect=self.dialect.name))

        return ddl + '\n);{rows}{constraints}{indexes}'.format(
            rows=str(RowCollection(self.table, dialect=self.dialect.name)),
            constraints=str(ConstraintCollection(self.table,
                                                 use_alter=True,
                                                 dialect=self.dialect.name)),
            indexes=str(IndexCollection(self.table,
                                        dialect=self.dialect.name)))


class Schema(Compiler):
    """SQL compiler class used to compile schemas."""

    def __init__(self, dialect: str = None):
        """
        Creates a new schema compiler instance.

        Args:
            dialect: The SQL dialect name to use
        """
        self.tables = types.List()

        super().__init__(dialect)

    def addTable(self, table: schema.Table, rows: types.List):
        """
        Add the given table to schema.

        Args:
            table: The Table instance to add
            rows: The table rows list
        """
        # pylint: disable=protected-access
        table.rows = rows

        # Workaround to render table indexes in the order they were declared
        table._sorted_indexes = types.List([index
                                            for column in table.columns
                                            for index in table.indexes
                                            if column in iter(index.columns)])

        self.tables.append(table)

    @decorators.cachedmethod()
    def compile(self) -> str:
        """
        Compiles the SQL statements for the schema

        Returns:
            The compiled SQL statements for the schema
        """
        return '\n\n'.join([str(Table(table, dialect=self.dialect.name))
                            for table in self.tables])


class Dialect(object):
    """Utility class for retrieval of SQL dialect implementations."""

    @staticmethod
    def factory(dialect: str) -> interfaces.Dialect:
        """
        Factories the given SQL dialect instance by name.

        Args:
            dialect: The SQL dialect name

        Returns:
            The SQL dialect instance
        """
        if dialect == 'default':
            return default.DefaultDialect()

        if dialect in ('firebird', 'mssql', 'mysql', 'oracle', 'postgresql',
                       'sqlite', 'sybase'):
            return dialects.registry.load(dialect)()

        raise UnsupportedDialectError('Unsupported dialect: {}'.format(dialect))

    @staticmethod
    def getNamingConvention(dialect: interfaces.Dialect) -> dict:
        """
        Returns the naming convention used by a given SQL dialect.

        Args:
            dialect: The SQL dialect instance

        Returns:
            The SQL dialect naming convention
        """
        convention = {
            schema.PrimaryKeyConstraint: 'pk_{table_name}',
            schema.ForeignKeyConstraint: 'fk_{table_name}_{column_name}',
            schema.UniqueConstraint: 'uq_{table_name}_{column_name}',
            schema.Index: 'ix_{table_name}_{column_name}',
        }

        # Workaround for Firebird identifiers size limitation
        if dialect.name == 'firebird':
            convention = {key: value[:1] + value[2:]
                          for key, value in convention.items()}

        return convention


class UnsupportedDialectError(Exception):
    """Exception class raised when a given SQL dialect is not supported."""
