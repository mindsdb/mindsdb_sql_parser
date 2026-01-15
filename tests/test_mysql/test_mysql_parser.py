from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.parser import Show
from mindsdb_sql_parser.ast import Select, Identifier, BinaryOperation, Star, Variable, Function, ASTNode


def compare_ast(parsed: ASTNode, expected: ASTNode, sql: str) -> None:
    assert parsed.to_tree() == expected.to_tree()
    assert str(parsed).lower() == sql.lower()
    assert str(parsed) == str(expected)
    assert str(eval(parsed.to_tree())) == str(parsed)


class TestMySQLParser:
    def test_select_variable(self):
        sql = 'SELECT @version'
        ast = parse_sql(sql)
        expected_ast = Select(targets=[Variable('version')])
        compare_ast(ast, expected_ast, sql)

        sql = 'SELECT @@version'
        ast = parse_sql(sql)
        expected_ast = Select(targets=[Variable('version', is_system_var=True)])
        compare_ast(ast, expected_ast, sql)

    def test_select_varialbe_complex(self):
        sql = """SELECT * FROM tab1 WHERE column1 in (SELECT column2 + @variable FROM t2)"""
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
        compare_ast(ast, expected_ast, sql)

    def test_show_index(self):
        sql = "SHOW INDEX FROM `predictors`"
        ast = parse_sql(sql)
        expected_ast = Show(
            category='INDEX',
            from_table=Identifier('`predictors`')
        )
        compare_ast(ast, expected_ast, sql)

    def test_show_index_from_db(self):
        sql = "SHOW INDEX FROM `predictors` FROM db"
        ast = parse_sql(sql)
        expected_ast = Show(
            category='INDEX',
            from_table=Identifier('db.`predictors`'),
        )
        compare_ast(ast, expected_ast, sql)

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
        compare_ast(ast, expected_ast, sql)

    def test_with_rollup_multiple_columns(self):
        """Test WITH ROLLUP with multiple GROUP BY columns"""
        sql = "SELECT year, country, SUM(sales) FROM booksales GROUP BY year, country WITH ROLLUP"

        ast = parse_sql(sql)
        expected_ast = Select(
            targets=[
                Identifier('year'),
                Identifier('country'),
                Function(op='SUM', args=[Identifier('sales')])
            ],
            from_table=Identifier('booksales'),
            group_by=[
                Identifier('year'),
                Identifier('country', with_rollup=True)
            ]
        )
        compare_ast(ast, expected_ast, sql)
