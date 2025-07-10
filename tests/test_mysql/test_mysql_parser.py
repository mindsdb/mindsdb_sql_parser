from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast import Select, Identifier, BinaryOperation, Star
from mindsdb_sql_parser.ast import Variable, Function
from mindsdb_sql_parser.parser import Show


class TestMySQLParser:
    def test_select_variable(self):
        sql = 'SELECT @version'
        ast = parse_sql(sql)
        expected_ast = Select(targets=[Variable('version')])
        assert ast.to_tree() == expected_ast.to_tree()
        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)

        sql = 'SELECT @@version'
        ast = parse_sql(sql)
        expected_ast = Select(targets=[Variable('version', is_system_var=True)])
        assert ast.to_tree() == expected_ast.to_tree()
        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)

    def test_select_varialbe_complex(self):
        sql = f"""SELECT * FROM tab1 WHERE column1 in (SELECT column2 + @variable FROM t2)"""
        ast = parse_sql(sql)
        expected_ast = Select(targets=[Star()],
                              from_table=Identifier('tab1'),
                              where=BinaryOperation(op='in',
                                                    args=(
                                                        Identifier('column1'),
                                                        Select(targets=[BinaryOperation(op='+',
                                                                                        args=[Identifier('column2'),
                                                                                              Variable('variable')])
                                                                        ],
                                                               from_table=Identifier('t2'),
                                                               parentheses=True)
                                                    )
                                                    ))

        assert ast.to_tree() == expected_ast.to_tree()
        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)

    def test_show_index(self):
        sql = "SHOW INDEX FROM `predictors`"
        ast = parse_sql(sql)
        expected_ast = Show(
            category='INDEX',
            from_table=Identifier('`predictors`')
        )

        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_show_index_from_db(self):
        sql = "SHOW INDEX FROM `predictors` FROM db"
        ast = parse_sql(sql)
        expected_ast = Show(
            category='INDEX',
            from_table=Identifier('db.`predictors`'),
        )

        # assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_with_rollup(self):
        sql = "SELECT country, SUM(sales) FROM booksales GROUP BY country WITH ROLLUP"

        ast = parse_sql(sql)
        expected_ast = Select(
            targets=[
                Identifier('country'),
                Function(op='SUM', args=[Identifier('sales')])
            ],
            from_table=Identifier('booksales'),
            group_by=[Identifier('country', with_rollup=True)]
        )

        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()
