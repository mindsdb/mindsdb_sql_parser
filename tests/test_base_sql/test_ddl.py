import pytest

from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast import *

class TestDDL:

    def test_drop_database(self):

        sql = "DROP DATABASE IF EXISTS dbname"

        ast = parse_sql(sql)
        expected_ast = DropDatabase(name=Identifier('dbname'), if_exists=True)

        assert str(ast).lower() == sql.lower()
        assert ast.to_tree() == expected_ast.to_tree()

        sql = "DROP DATABASE dbname"

        ast = parse_sql(sql)
        expected_ast = DropDatabase(name=Identifier('dbname'), if_exists=False)

        assert str(ast).lower() == sql.lower()
        assert ast.to_tree() == expected_ast.to_tree()

        # DROP SCHEMA is a synonym for DROP DATABASE.
        sql = "DROP SCHEMA dbname"

        ast = parse_sql(sql)
        expected_ast = DropDatabase(name=Identifier('dbname'))

        assert str(ast).lower() == 'DROP DATABASE dbname'.lower()
        assert ast.to_tree() == expected_ast.to_tree()

    def test_drop_view(self):

        sql = "DROP VIEW IF EXISTS vname1, vname2"

        ast = parse_sql(sql)
        expected_ast = DropView(names=[Identifier('vname1'), Identifier('vname2')], if_exists=True)

        assert str(ast).lower() == sql.lower()
        assert ast.to_tree() == expected_ast.to_tree()

        sql = "DROP VIEW vname"

        ast = parse_sql(sql)
        expected_ast = DropView(names=[Identifier('vname')], if_exists=False)

        assert str(ast).lower() == sql.lower()
        assert ast.to_tree() == expected_ast.to_tree()

    def test_drop_predictor_table_syntax_ok(self):
        sql = "DROP TABLE mindsdb.tbl"
        ast = parse_sql(sql)
        expected_ast = DropTables(tables=[Identifier('mindsdb.tbl')])
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

        sql = "DROP TABLE if exists mindsdb.tbl"
        ast = parse_sql(sql)
        expected_ast = DropTables(tables=[Identifier('mindsdb.tbl')], if_exists=True)
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()


