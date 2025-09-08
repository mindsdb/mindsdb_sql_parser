from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast.mindsdb import *
from mindsdb_sql_parser.ast import *


class TestChatbots:
    def test_test_create_chatbot(self):
        sql = '''
            create chatbot mybot
            using 
            model = 'chat_model', 
            database ='my_rocket_chat',
            agent = 'my_agent'
        '''
        ast = parse_sql(sql)
        expected_ast = CreateChatBot(
            name=Identifier('mybot'),
            database=Identifier('my_rocket_chat'),
            model=Identifier('chat_model'),
            agent=Identifier('my_agent')
        )
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_test_create_chatbot_with_params(self):
        sql = '''
            create chatbot mybot
            using 
            model = 'chat_model', 
            database ='my_rocket_chat',
            key = 'value'
        '''
        ast = parse_sql(sql)
        expected_ast = CreateChatBot(
            name=Identifier('mybot'),
            database=Identifier('my_rocket_chat'),
            model=Identifier('chat_model'),
            agent=None,
            params={'key': 'value'}
        )
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_update_chatbot(self):
        sql = '''
            update chatbot mybot
            set
            name = 'new_name',
            model = 'new_model',
            database = 'new_database',
            chat_engine = 'new_chat_engine',
            is_running = true,
            new_param = 'new_value'
        '''
        ast = parse_sql(sql)
        expected_params = {
            'name': 'new_name',
            'model': 'new_model',
            'database': 'new_database',
            'chat_engine': 'new_chat_engine',
            'is_running': True,
            'new_param': 'new_value'
        }
        expected_ast = UpdateChatBot(
            name=Identifier('mybot'),
            updated_params=expected_params
        )
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_drop_chatbot(self):
        sql = '''
            drop chatbot mybot
        '''
        ast = parse_sql(sql)
        expected_ast = DropChatBot(
            name=Identifier('mybot'),
        )
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_create_chatbot_case_handling(self):
        sql = """
            CREATE CHATBOT my_chatbot
            USING
                DaTaBaSe = 'my_db',
                MoDeL = 'my_model',
                AgEnT = 'my_agent'
        """
        ast = parse_sql(sql)
        expected_ast = CreateChatBot(
            name=Identifier('my_chatbot'),
            database=Identifier('my_db'),
            model=Identifier('my_model'),
            agent=Identifier('my_agent')
        )
        assert ast.to_tree() == expected_ast.to_tree()

    def test_update_chatbot_case_handling(self):
        sql = """
            UPDATE CHATBOT my_chatbot
            SET
                MoDeL = 'new_model'
        """
        ast = parse_sql(sql)
        expected_ast = UpdateChatBot(
            name=Identifier('my_chatbot'),
            updated_params={'model': 'new_model'}
        )
        assert ast.to_tree() == expected_ast.to_tree()