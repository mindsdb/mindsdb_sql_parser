import pytest

from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast import *


class TestCreate:
    def test_create_from_select(self):
        expected_ast = CreateTable(
            name=Identifier('int1.model_name'),
            is_replace=True,
            from_select=Select(
                targets=[Identifier('a')],
                from_table=Identifier('ddd'),
            )
        )

        # with parens
        sql = '''
         create or replace table int1.model_name (
            select a from ddd             
        )
        '''
        ast = parse_sql(sql)

        assert str(ast).lower() == str(expected_ast).lower()
        assert ast.to_tree() == expected_ast.to_tree()

        # without parens
        sql = '''
         create or replace table int1.model_name
            select a from ddd             
        '''
        ast = parse_sql(sql)

        assert str(ast).lower() == str(expected_ast).lower()
        assert ast.to_tree() == expected_ast.to_tree()

        expected_ast.is_replace = False

        # no replace
        sql = '''
         create table int1.model_name
            select a from ddd             
        '''
        ast = parse_sql(sql)

        assert str(ast).lower() == str(expected_ast).lower()
        assert ast.to_tree() == expected_ast.to_tree()


class TestCreateMindsdb:

    def test_create(self):

        for is_replace in [True, False]:
            for if_not_exists in [True, False]:

                expected_ast = CreateTable(
                    name=Identifier('mydb.Persons'),
                    is_replace=is_replace,
                    if_not_exists=if_not_exists,
                    columns=[
                        TableColumn(name='PersonID', type='int'),
                        TableColumn(name='LastName', type='varchar', length=255),
                        TableColumn(name='FirstName', type='char', length=10),
                        TableColumn(name='Info', type='json'),
                        TableColumn(name='City', type='varchar'),
                    ]
                )
                replace_str = 'OR REPLACE' if is_replace else ''
                exist_str = 'IF NOT EXISTS' if if_not_exists else ''

                sql = f'''
                 CREATE {replace_str} TABLE {exist_str} mydb.Persons(
                    PersonID int,
                    LastName varchar(255),
                    FirstName char(10),
                    Info json,
                    City varchar
                 )
                '''
                ast = parse_sql(sql)

                assert str(ast).lower() == str(expected_ast).lower()
                assert ast.to_tree() == expected_ast.to_tree()

        # test with primary keys / defaults
        # using serial

        sql = f'''
         CREATE TABLE mydb.Persons(
            PersonID serial,
            active BOOL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP            
         )
        '''
        ast = parse_sql(sql)

        expected_ast = CreateTable(
            name=Identifier('mydb.Persons'),
            columns=[
                TableColumn(name='PersonID', type='serial'),
                TableColumn(name='active', type='BOOL', nullable=False),
                TableColumn(name='created_at', type='TIMESTAMP', default='CURRENT_TIMESTAMP'),
            ]
        )

        assert str(ast).lower() == str(expected_ast).lower()
        assert ast.to_tree() == expected_ast.to_tree()

        # using primary key column

        sql = f'''
         CREATE TABLE mydb.Persons(
            PersonID INT PRIMARY KEY,
            name TEXT NULL   
         )
        '''
        ast = parse_sql(sql)

        expected_ast = CreateTable(
            name=Identifier('mydb.Persons'),
            columns=[
                TableColumn(name='PersonID', type='INT', is_primary_key=True),
                TableColumn(name='name', type='TEXT', nullable=True),
            ]
        )

        assert str(ast).lower() == str(expected_ast).lower()
        assert ast.to_tree() == expected_ast.to_tree()

        # multiple primary keys

        sql = f'''
         CREATE TABLE mydb.Persons(
            location_id INT,
            num INT,
            name TEXT,
            PRIMARY KEY (location_id, num)  
         )
        '''
        ast = parse_sql(sql)

        expected_ast = CreateTable(
            name=Identifier('mydb.Persons'),
            columns=[
                TableColumn(name='location_id', type='INT', is_primary_key=True),
                TableColumn(name='num', type='INT', is_primary_key=True),
                TableColumn(name='name', type='TEXT'),
            ]
        )

        assert str(ast).lower() == str(expected_ast).lower()
        assert ast.to_tree() == expected_ast.to_tree()

