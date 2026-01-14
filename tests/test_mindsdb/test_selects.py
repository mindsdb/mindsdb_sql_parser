import pytest
from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast import *
from mindsdb_sql_parser.utils import JoinType


class TestSpecificSelects:
    def test_select_from_predictors(self):
        sql = "SELECT * FROM predictors WHERE name = 'pred_name'"
        ast = parse_sql(sql)
        expected_ast = Select(
            targets=[Star()],
            from_table=Identifier('predictors'),
            where=BinaryOperation('=', args=[Identifier('name'), Constant('pred_name')])
        )

        # assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_select_predict_column(self):
        sql = "SELECT predict FROM mindsdb.predictors"
        ast = parse_sql(sql)
        expected_ast = Select(
            targets=[Identifier('predict')],
            from_table=Identifier('mindsdb.predictors'),
        )

        # assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_select_status_column(self):
        sql = "SELECT status FROM mindsdb.predictors"
        ast = parse_sql(sql)
        expected_ast = Select(
            targets=[Identifier('status')],
            from_table=Identifier('mindsdb.predictors'),
        )

        # assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_native_query(self):
        sql = """
           SELECT status 
           FROM int1 (select q from p from r where x = 'test''test')
           group by 1
           limit 1
        """
        ast = parse_sql(sql)
        expected_ast = Select(
            targets=[Identifier('status')],
            from_table=NativeQuery(
                integration=Identifier('int1'),
                query="select q from p from r where x = 'test''test'"
            ),
            limit=Constant(1),
            group_by=[Constant(1)]
        )

        # assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_select_using(self):
        sql = """
           SELECT status FROM tbl1
           group by 1
           using p1=1, p2='2', p3=column
        """
        ast = parse_sql(sql)
        expected_select = Select(
            targets=[Identifier('status')],
            from_table=Identifier('tbl1'),
            group_by=[Constant(1)],
            using={
                'p1': 1,
                'p2': '2',
                'p3': Identifier('column')
            }
        )

        assert str(ast) == str(expected_select)
        assert ast.to_tree() == expected_select.to_tree()

        sql = """
           insert into int2.table2
            (
             SELECT status FROM tbl1
             group by 1
            )
           using p1=1, p2='2', p3=column
        """
        ast = parse_sql(sql)
        expected_ast = Insert(
            table=Identifier('int2.table2'),
            from_select=expected_select
        )

        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()


    def test_join_using(self):
        sql = """
           SELECT status FROM tbl1
           join pred1
           using p1=1, p2='2'
        """
        ast = parse_sql(sql)
        expected_ast = Select(
            targets=[Identifier('status')],
            from_table=Join(
                left=Identifier('tbl1'),
                right=Identifier('pred1'),
                join_type=JoinType.JOIN
            ),
            using={
                'p1': 1,
                'p2': '2'
            }
        )

        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_select_limit_negative(self):
        sql = """SELECT * FROM t1 LIMIT -1"""

        ast = parse_sql(sql)
        expected_ast = Select(targets=[Star()],
                              from_table=Identifier(parts=['t1']),
                              limit=Constant(-1))

        assert ast.to_tree() == expected_ast.to_tree()
        assert str(ast) == str(expected_ast)

    def test_last(self):
        sql = """SELECT * FROM t1 t where t.id>last and t.x > coalence(last, 0)"""

        ast = parse_sql(sql)
        expected_ast = Select(
            targets=[Star()],
            from_table=Identifier(parts=['t1'], alias=Identifier('t')),
            where=BinaryOperation(op='and', args=[
                BinaryOperation(
                  op='>',
                  args=[
                      Identifier(parts=['t', 'id']),
                      Last()
                  ]
                ),
                BinaryOperation(
                  op='>',
                  args=[
                      Identifier(parts=['t', 'x']),
                      Function(op='coalence', args=[
                          Last(),
                          Constant(0)
                      ])
                  ]
                ),
            ])
        )

        assert ast.to_tree() == expected_ast.to_tree()
        assert str(ast) == str(expected_ast)


        sql = """SELECT last(a) FROM t1"""

        ast = parse_sql(sql)
        expected_ast = Select(
            targets=[Function(
                op='last',
                args=[Identifier('a')]
            )],
            from_table=Identifier(parts=['t1']),
        )

        assert ast.to_tree() == expected_ast.to_tree()
        assert str(ast) == str(expected_ast)

    def test_json(self):
        sql = """SELECT col->1->>'c' from TAB1"""

        ast = parse_sql(sql)
        expected_ast = Select(
            targets=[BinaryOperation(
                op='->>',
                args=[
                    BinaryOperation(
                        op='->',
                        args=[
                            Identifier('col'),
                            Constant(1)
                        ]
                    ),
                    Constant('c')
                ]
            )],
            from_table=Identifier(parts=['TAB1']),
        )

        assert ast.to_tree() == expected_ast.to_tree()
        assert str(ast) == str(expected_ast)

    def test_vector(self):
        for op in ['<->', '<+>', '<#>', '<=>', '<~>', '<%>']:
            sql = f"SELECT * from TAB1 WHERE embedding {op} '[3,1,2]'"

            ast = parse_sql(sql)
            expected_ast = Select(
                targets=[Star()],
                where=BinaryOperation(
                    op=op,
                    args=[
                        Identifier('embedding'),
                        Constant('[3,1,2]')
                    ]
                ),
                from_table=Identifier(parts=['TAB1']),
            )

            assert ast.to_tree() == expected_ast.to_tree()
            assert str(ast) == str(expected_ast)

    def test_match(self):
        sql = "SELECT a~b, a!~c from TAB1"

        ast = parse_sql(sql)
        expected_ast = Select(
            targets=[
                BinaryOperation(op='~', args=[Identifier('a'), Identifier('b')]),
                BinaryOperation(op='!~', args=[Identifier('a'), Identifier('c')]),
            ],
            from_table=Identifier(parts=['TAB1']),
        )

        assert ast.to_tree() == expected_ast.to_tree()
        assert str(ast) == str(expected_ast)

    def test_array(self):
        for op in ['@>', '<@', '&&']:
            sql = f"SELECT * from TAB1 WHERE a {op} b"

            ast = parse_sql(sql)
            expected_ast = Select(
                targets=[Star()],
                where=BinaryOperation(
                    op=op,
                    args=[
                        Identifier('a'),
                        Identifier('b')
                    ]
                ),
                from_table=Identifier(parts=['TAB1']),
            )

            assert ast.to_tree() == expected_ast.to_tree()
            assert str(ast) == str(expected_ast)
