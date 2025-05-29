from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast.mindsdb import *
from mindsdb_sql_parser.ast import *
from mindsdb_sql_parser.lexer import MindsDBLexer

class TestViews:
    def test_create_view_lexer(self):
        sql = "CREATE VIEW my_view FROM integration AS ( SELECT * FROM pred )"
        tokens = list(MindsDBLexer().tokenize(sql))
        assert tokens[0].value == 'CREATE'
        assert tokens[0].type == 'CREATE'

        assert tokens[1].value == 'VIEW'
        assert tokens[1].type == 'VIEW'

    def test_create_view_full(self):
        sql = "CREATE VIEW IF NOT EXISTS my_view FROM integr AS ( SELECT * FROM pred )"
        ast = parse_sql(sql)
        expected_ast = CreateView(name=Identifier('my_view'),
                                  if_not_exists=True,
                                  from_table=Identifier('integr'),
                                  query_str="SELECT * FROM pred")

        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_create_view_nofrom(self):
        sql = "CREATE VIEW my_view ( SELECT * FROM pred )"
        ast = parse_sql(sql)
        expected_ast = CreateView(name=Identifier('my_view'),
                                  query_str="SELECT * FROM pred")

        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_alter_view_full(self):
        sql = "ALTER VIEW my_view FROM integr AS ( SELECT * FROM pred )"
        ast = parse_sql(sql)
        expected_ast = AlterView(
            name=Identifier('my_view'),
            from_table=Identifier('integr'),
            query_str="SELECT * FROM pred"
        )
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_alter_view_nofrom(self):
        sql = "ALTER VIEW my_view AS ( SELECT * FROM pred )"
        ast = parse_sql(sql)
        expected_ast = AlterView(
            name=Identifier('my_view'),
            query_str="SELECT * FROM pred"
        )
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    # def test_create_dataset_full(self):
    #     sql = "CREATE DATASET my_view FROM integr AS ( SELECT * FROM pred )"
    #     ast = parse_sql(sql)
    #     expected_ast = CreateView(name='my_view',
    #                               from_table=Identifier('integr'),
    #                               query_str="SELECT * FROM pred")
    #
    #     assert str(ast) == str(expected_ast)
    #     assert ast.to_tree() == expected_ast.to_tree()

    # def test_create_dataset_nofrom(self):
    #     sql = "CREATE DATASET my_view ( SELECT * FROM pred )"
    #     ast = parse_sql(sql)
    #     expected_ast = CreateView(name='my_view',
    #                               query_str="SELECT * FROM pred")

        # assert str(ast) == str(expected_ast)
        # assert ast.to_tree() == expected_ast.to_tree()
