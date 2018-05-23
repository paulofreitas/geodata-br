#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
SQL file format utils module
'''
from __future__ import absolute_import, unicode_literals

# Imports

# External compatibility dependencies

from builtins import str
from future.utils import iteritems

# External dependencies

from sqlalchemy import dialects, util
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.exc import CompileError
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import crud, elements
from sqlalchemy.sql.ddl import AddConstraint, CreateColumn, CreateIndex, \
                               CreateTable
from sqlalchemy.sql.dml import Insert
from sqlalchemy.sql.schema import Column, ForeignKeyConstraint, Index, \
                                  PrimaryKeyConstraint

# Package dependencies

from places.core.i18n import _, Translator

# Translator setup

Translator.load('databases')

# Classes


class SchemaGenerator(object):
    '''
    SQL schema generator class.
    '''

    minified = False

    def __init__(self, dialect='default', minified=False):
        '''
        Constructor.

        Arguments:
            dialect (str): The SQL dialect to use
            minified (bool): Whether the SQL statements should be minified
                or not
        '''
        self.tables = []
        self.dialect = dialect
        self._dialect = self.getDialect(dialect)

        SchemaGenerator.minified = minified

    @staticmethod
    def getDialect(dialect):
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

        raise Exception('Unsupported dialect: {}'.format(dialect))

    # Custom DDL/DML compilers

    @staticmethod
    @compiles(CreateColumn)
    def __compileCreateColumn(create, compiler, **kw):
        '''
        Compiles the CREATE TABLE columns statements.
        '''
        column = create.element

        ddl = '{} {}'.format(_(column.name),
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
        '''
        Compiles the CREATE TABLE statements.
        '''
        table = create.element
        separator = '' if SchemaGenerator.minified else '\n'
        first_pk = False

        ddl = 'CREATE '

        if table._prefixes:
            ddl += ' '.join(table._prefixes) + ' '

        ddl += 'TABLE ' + SchemaGenerator.formatTable(table, compiler.preparer)
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
        '''
        Compiles CREATE INDEX statements.
        '''
        index = create.element

        compiler._verify_index_table(index)

        ddl = 'CREATE '
        separator = ',' if SchemaGenerator.minified else ', '

        if index.unique:
            ddl += 'UNIQUE '

        ddl += 'INDEX {} ON {}'.format(
            SchemaGenerator.formatIndex(index,
                                        compiler.preparer,
                                        include_schema=include_schema),
            SchemaGenerator.formatTable(index.table,
                                        compiler.preparer,
                                        use_schema=include_table_schema)
        )

        if not SchemaGenerator.minified:
            ddl += ' '

        ddl += '({});'.format(separator.join(
            compiler.process(expression,
                             include_table=False,
                             literal_binds=True)
            for expression in index.expressions
        ))

        return ddl

    @staticmethod
    @compiles(Column)
    def __compileColumn(column,
                        compiler,
                        add_to_result_map=None,
                        include_table=True,
                        **options):
        name = orig_name = column.name

        if name is None:
            raise CompileError('Cannot compile Column object until'
                               " its 'name' is assigned.")

        is_literal = column.is_literal

        if not is_literal and isinstance(name, elements._truncated_label):
            name = compiler._truncated_identifier('colident', name)

        if add_to_result_map is not None:
            add_to_result_map(
                name,
                orig_name,
                (column, name, column.key),
                column.type
            )

        if is_literal:
            name = compiler.escape_literal_column(name) if is_literal \
                else compiler.preparer.quote(name)

        table = column.table

        if table is None or not include_table or not table.named_with_column:
            return _(name)

        schema_prefix = '' if not table.schema \
            else compiler.preparer.quote_schema(table.schema) + '.' \

        table_name = table.name

        if isinstance(table_name, elements._truncated_label):
            table_name = compiler._truncated_identifier('alias', table_name)

        return schema_prefix + compiler.preparer.quote(_(table_name)) + '.' + _(name)

    @staticmethod
    @compiles(AddConstraint)
    def __compileAddConstraint(constraint, compiler):
        '''
        Compiles ALTER TABLE ADD CONSTRAINT statements.
        '''
        return 'ALTER TABLE {} ADD {};'.format(
            SchemaGenerator.formatTable(constraint.element.table, compiler.preparer),
            compiler.process(constraint.element)
        )

    @staticmethod
    @compiles(PrimaryKeyConstraint)
    def __compilePrimaryKeyConstraint(constraint, compiler):
        '''
        Compiles PRIMARY KEY constraint statements.
        '''
        if len(constraint) == 0:
            return ''

        ddl = ''
        separator = ',' if SchemaGenerator.minified else ', '

        if constraint.name is not None:
            formatted_name = SchemaGenerator.formatConstraint(constraint,
                                                              compiler.preparer)

            if formatted_name is not None:
                ddl += 'CONSTRAINT {} '.format(formatted_name)

        ddl += 'PRIMARY KEY'

        if not SchemaGenerator.minified:
            ddl += ' '

        ddl += '({})'.format(separator.join(
            compiler.preparer.quote(_(_constraint.name))
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
        '''
        Compiles FOREIGN KEY constraint statements.
        '''
        ddl = ''
        separator = ',' if SchemaGenerator.minified else ', '

        if constraint.name is not None:
            formatted_name = SchemaGenerator.formatConstraint(constraint,
                                                              compiler.preparer)

            if formatted_name is not None:
                ddl += 'CONSTRAINT {} '.format(formatted_name)

        remote_table = list(constraint.elements)[0].column.table

        ddl += 'FOREIGN KEY'

        if not SchemaGenerator.minified:
            ddl += ' '

        ddl += '({}) REFERENCES {}'.format(
            separator.join(
                compiler.preparer.quote(_(element.parent.name))
                for element in constraint.elements
            ),
            SchemaGenerator.formatTable(remote_table, compiler.preparer)
        )

        if not SchemaGenerator.minified:
            ddl += ' '

        ddl += '({})'.format(separator.join(
            compiler.preparer.quote(_(element.column.name))
            for element in constraint.elements
        ))
        ddl += compiler.define_constraint_match(constraint)
        ddl += compiler.define_constraint_cascades(constraint)
        ddl += compiler.define_constraint_deferrability(constraint)

        return ddl

    @staticmethod
    @compiles(Insert)
    def __compileInsert(insert_stmt, compiler, **options):
        '''
        Compiles INSERT statements.
        '''
        compiler.stack.append({
            'correlate_froms': set(),
            'asfrom_froms': set(),
            'selectable': insert_stmt,
        })
        compiler.isinsert = True
        crud_params = crud._get_crud_params(compiler, insert_stmt, **options)

        if not crud_params:
            return

        if insert_stmt._has_multi_parameters \
                and not compiler.dialect.supports_multivalues_insert:
            return

        dml = 'INSERT INTO ' + SchemaGenerator.formatTable(insert_stmt.table,
                                                           compiler.preparer)
        separator = ',' if SchemaGenerator.minified else ', '

        if insert_stmt.select is not None:
            dml += ' {}'.format(
                compiler.process(compiler._insert_from_select, **options))
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

    # Custom DDL formatters

    @staticmethod
    def formatTable(table, preparer, use_schema=True, name=None):
        '''
        Prepares a quoted table and schema name.
        '''
        if name is None:
            name = _(table.name)

        result = preparer.quote(name)

        if not preparer.omit_schema and use_schema \
                and getattr(table, 'schema', None):
            result = preparer.quote_schema(table.schema) + '.' + result

        return result

    @staticmethod
    @util.dependencies('sqlalchemy.sql.naming')
    def formatConstraint(naming, constraint, preparer):
        if isinstance(constraint.name, elements._defer_name):
            name = naming._constraint_name_for_table(constraint,
                                                     constraint.table)
            if name:
                return preparer.quote(_(name))
            elif isinstance(constraint.name, elements._defer_none_name):
                return None

        return preparer.quote(_(constraint.name))

    @staticmethod
    def formatIndex(index, preparer, include_schema=False):
        if include_schema and index.table is not None and index.table.schema:
            schema = index.table.schema
            schema_name = preparer.quote_schema(schema)
        else:
            schema_name = None

        index_name = preparer.quote(_(index.name))

        if schema_name:
            index_name = schema_name + '.' + index_name

        return index_name

    # Custom DDL renderers

    def render(self, createIndexes=True):
        '''
        Render all SQL statements for the instance tables.

        Arguments:
            createIndexes (bool): Whether or not it should create table indexes

        Returns:
            string: The compiled SQL statements
        '''
        separator = '' if self.minified else '\n\n'

        return separator.join([
            self.renderCreateTable(table, createIndexes=createIndexes)
            for table in self.tables
        ])

    def renderCreateTable(self, table, createIndexes=True):
        '''
        Render the CREATE TABLE statement for the given table.

        Arguments:
            table (sqlalchemy.sql.schema.Table:): The SQLAlchemy Table object to
                render
            createIndexes (bool): Whether or not it should create table indexes

        Returns:
            string: The compiled CREATE TABLE statement
        '''
        ddl = []
        separator = '' if self.minified else '\n'

        if not self.minified:
            ddl.append('--\n-- Structure for table {}\n--\n'.format(_(table.name)))

        ddl.append(str(CreateTable(table).compile(dialect=self._dialect)))

        if len(table._data):
            ddl.append(separator + self.renderInserts(table))

        if len(table.foreign_keys) and self._dialect.supports_alter:
            ddl.append(separator + self.renderTableConstraints(table))

        if createIndexes and len(table.indexes):
            ddl.append(separator + self.renderTableIndexes(table))

        return separator.join(ddl)

    def renderInserts(self, table):
        '''
        Render the INSERT statements for the given table.

        Arguments:
            table (sqlalchemy.sql.schema.Table:): The SQLAlchemy Table object to
                render

        Returns:
            string: The compiled INSERT statements
        '''
        ddl = []
        separator = '' if self.minified else '\n'

        if not self.minified:
            ddl.append('--\n-- Data for table {}\n--\n'.format(_(table.name)))

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
        '''
        Render the ALTER TABLE ADD CONSTRAINT statements for the given table.

        Arguments:
            table (sqlalchemy.sql.schema.Table:): The SQLAlchemy Table object to
                render

        Returns:
            string: The compiled ALTER TABLE ADD CONSTRAINT statements
        '''
        if not self._dialect.supports_alter:
            return

        ddl = []
        separator = '' if self.minified else '\n'

        if not self.minified:
            ddl.append('--\n-- Constraints for table {}\n--\n' \
                .format(_(table.name)))

        for constraint in table._sorted_constraints:
            if isinstance(constraint, ForeignKeyConstraint):
                ddl.append(str(
                    AddConstraint(constraint).compile(dialect=self._dialect)
                ))

        return separator.join(ddl)

    def renderTableIndexes(self, table):
        '''
        Render the CREATE INDEXES statements for the given table.

        Arguments:
            table (sqlalchemy.sql.schema.Table:): The SQLAlchemy Table object to
                render

        Returns:
            string: The compiled CREATE INDEXES statements
        '''
        ddl = []
        separator = '' if self.minified else '\n'

        if not self.minified:
            ddl.append('--\n-- Indexes for table {}\n--\n'.format(_(table.name)))

        for index in table._sorted_indexes:
            ddl.append(str(CreateIndex(index).compile(dialect=self._dialect)))

        return separator.join(ddl)

    # Methods

    def createTable(self, entity):
        '''
        Add the given entity table to schema.

        Arguments:
            entity: The SQLAlchemy entity object

        Returns:
            sqlalchemy.sql.schema.Table: The SQLAlchemy table object
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
        '''
        String representation of this object.
        '''
        return self.render()
