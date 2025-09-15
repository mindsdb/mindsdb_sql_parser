from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast import *
from mindsdb_sql_parser.utils import JoinType


class TestOracle:
    def test_left_outer_join_render_skip(self):
        sql = "SELECT * FROM customer, orders "\
              "WHERE c_custkey = o_custkey(+)"

        ast = parse_sql(sql)
        expected_ast = Select(
            targets=[Star()],
            from_table=Join(left=Identifier('customer'),
                            right=Identifier('orders'),
                            join_type=JoinType.INNER_JOIN,
                            implicit=True),
            where=BinaryOperation('=', args=[
                Identifier('c_custkey'), Identifier('o_custkey', is_outer=True)
            ]),
        )

        # don't render (+)
        assert str(ast).lower() == sql.replace('(+)', '').lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

        assert ast.where.args[1].is_outer is True

    def test_limit(self):
        for keyword in ('NEXT', 'FIRST'):
            sql = f"SELECT * FROM customer FETCH  {keyword} 10 ROWS ONLY"

            ast = parse_sql(sql)
            expected_ast = Select(
                targets=[Star()],
                from_table=Identifier('customer'),
                limit=Constant(10)
            )

            assert str(ast) == str(expected_ast)
            assert ast.to_tree() == expected_ast.to_tree()
