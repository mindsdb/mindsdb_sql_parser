from mindsdb_sql_parser.lexer import MindsDBLexer


class TestMySQLLexer:
    def test_select_variable(self):
        sql = f'SELECT @version'
        tokens = list(MindsDBLexer().tokenize(sql))

        assert tokens[0].type == 'SELECT'
        assert tokens[0].value == 'SELECT'

        assert tokens[1].type == 'VARIABLE'
        assert tokens[1].value == 'version'

    def test_select_system_variable(self):
        sql = f'SELECT @@version'
        tokens = list(MindsDBLexer().tokenize(sql))

        assert tokens[0].type == 'SELECT'
        assert tokens[0].value == 'SELECT'

        assert tokens[1].type == 'SYSTEM_VARIABLE'
        assert tokens[1].value == 'version'
