from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast import *


class TestParameters:
    def test_select_with_parameter_in_where(self):
        sql = "SELECT * FROM tbl WHERE col = ?"
        ast = parse_sql(sql)
        assert str(ast) == sql

    def test_select_multiple_parameters(self):
        sql = "SELECT * FROM tbl WHERE col1 > ? AND col2 = ?"
        ast = parse_sql(sql)
        assert str(ast) == sql

    def test_insert_with_parameters(self):
        sql = "INSERT INTO tbl_name(a, c) VALUES (?, ?)"
        ast = parse_sql(sql)
        assert str(ast) == sql

    def test_insert_with_multiple_parameter_rows(self):
        sql = "INSERT INTO tbl_name VALUES (?, ?), (?, ?)"
        ast = parse_sql(sql)
        assert str(ast) == sql
        
    def test_select_parameter_as_target(self):
        sql = "SELECT ?"
        ast = parse_sql(sql)
        assert str(ast) == sql

    def test_named_parameters(self):
        sql = "SELECT :a, max(1-:second_param), ? from t where x=:col_1"
        ast = parse_sql(sql)

        expected = Select(
            targets=[
                Parameter("a"),
                Function("max", args=[
                    BinaryOperation(op="-", args=[
                        Constant(1),
                        Parameter("second_param")
                    ])
                ]),
                Parameter("?")
            ],
            from_table=Identifier("t"),
            where=BinaryOperation(op="=", args=[
                Identifier("x"),
                Parameter("col_1")
            ])
        )

        assert str(ast) == str(expected)
