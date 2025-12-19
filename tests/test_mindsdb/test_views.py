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

    def test_create_view_with_variables(self):
        """Test multiple variables in view query"""
        query_str = "SELECT @var1, @@sys_var FROM tbl WHERE x = @var2"
        sql = f"CREATE VIEW v1 AS ({query_str})"
        ast = parse_sql(sql)
        
        # Check that all variables preserve their prefixes
        assert '@var1' in ast.query_str
        assert '@@sys_var' in ast.query_str
        assert '@var2' in ast.query_str
        assert ast.query_str == query_str

    def test_alter_view_with_variables(self):
        """Test that @ prefix is preserved in ALTER VIEW query_str"""
        query_str = "SELECT @var1, @@sys_var FROM tbl WHERE x = @var2"
        sql = f"ALTER VIEW myview AS ({query_str})"
        ast = parse_sql(sql)
        
        expected_ast = AlterView(
            name=Identifier('myview'),
            query_str=query_str
        )

        assert ast.query_str == query_str
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_create_view_with_using_clause(self):
        """Test CREATE VIEW with USING clause"""
        sql = 'create view test_view as (select * from local_mysql.test_house where sqft = @myvar) using test = 1, params = {"x": "y"}'
        ast = parse_sql(sql)

        assert ast.name.to_string() == 'test_view'
        assert ast.query_str == 'select * from local_mysql.test_house where sqft = @myvar'
        assert ast.using == {'test': 1, 'params': {'x': 'y'}}

    def test_alter_view_with_using_clause(self):
        """Test ALTER VIEW with USING clause"""
        sql = 'ALTER VIEW myview AS (select * from tbl) USING param1 = "value1", param2 = 123'
        ast = parse_sql(sql)
        
        assert ast.name.to_string() == 'myview'
        assert ast.query_str == 'select * from tbl'
        assert ast.using == {'param1': 'value1', 'param2': 123}

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
