from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast import *
from mindsdb_sql_parser.ast import Variable

class TestMDBParser:
    def test_select_variable(self):
        sql = 'SELECT @version'
        ast = parse_sql(sql)
        expected_ast = Select(targets=[Variable('version')])
        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)

        sql = 'SELECT @@version'
        ast = parse_sql(sql)
        expected_ast = Select(targets=[Variable('version', is_system_var=True)])
        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)

        sql = "set autocommit=1, global sql_mode=concat(@@sql_mode, ',STRICT_TRANS_TABLES'), NAMES utf8mb4 COLLATE utf8mb4_unicode_ci"
        ast = parse_sql(sql)
        expected_ast = Set(
            set_list=[
                Set(name=Identifier('autocommit'), value=Constant(1)),
                Set(name=Identifier('sql_mode'),
                    scope='global',
                    value=Function(op='concat', args=[
                        Variable('sql_mode', is_system_var=True),
                        Constant(',STRICT_TRANS_TABLES')
                    ])
                ),
                Set(category="NAMES",
                    value=Constant('utf8mb4', with_quotes=False),
                    params={'COLLATE': Constant('utf8mb4_unicode_ci', with_quotes=False)})
            ]
        )

        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)

    def test_set(self):
        for value in (0, 1, 'TRUE', 'FALSE', 'ON', 'OFF'):
            sql = f"set @@session.autocommit={value}"
            ast = parse_sql(sql)
            expected_ast = Set(
                name=Variable('session.autocommit', is_system_var=True),
                value=Constant(value, with_quotes=False)
            )
            assert str(ast).lower() == sql.lower()
            assert str(ast) == str(expected_ast)

    def test_mysql(self):
        sql = 'select @@session.auto_increment_increment, @@character_set_client'
        ast = parse_sql(sql)
        expected_ast = Select(
            targets=[
                Variable('session.auto_increment_increment', is_system_var=True),
                Variable('character_set_client', is_system_var=True),
            ]
        )

        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)

    def test_variables_in_select(self):
        """Test multiple variables in single query"""
        sql = "SELECT @var1, @var2 FROM tbl WHERE x = @var3 AND y = @@system_var"
        ast = parse_sql(sql)

        expected_ast = Select(
                targets=[Variable("var1"), Variable("var2")],
                from_table=Identifier("tbl"),
                where=BinaryOperation(
                    op="AND",
                    args=[
                        BinaryOperation(
                            op="=",
                            args=[Identifier("x"), Variable("var3")]
                        ),
                        BinaryOperation(
                            op="=",
                            args=[Identifier("y"), Variable("system_var", is_system_var=True)]
                        )
                    ]
                )
            )

        # Verify the string representation preserves all @ signs
        assert ast.to_tree() == expected_ast.to_tree()
        result = str(ast)
        assert result == str(expected_ast)
        assert "@var1" in result
        assert "@var2" in result
        assert "@var3" in result
        assert "@@system_var" in result