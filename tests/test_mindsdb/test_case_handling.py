import pytest
from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast import Identifier
from mindsdb_sql_parser.ast.mindsdb import (
    CreateSkill,
    UpdateSkill,
    CreateAgent,
    UpdateAgent,
    CreateChatBot,
    UpdateChatBot,
)

class TestParameterCasing:
    def test_create_skill_case_handling(self):
        sql = """
            CREATE SKILL my_skill
            USING
                TyPe = 'knowledge_base',
                SoUrCe = 'my_knowledge_base'
        """
        ast = parse_sql(sql)
        expected_ast = CreateSkill(
            name=Identifier('my_skill'),
            type='knowledge_base',
            params={'source': 'my_knowledge_base'}
        )
        assert ast.to_tree() == expected_ast.to_tree()

    def test_update_skill_case_handling(self):
        sql = """
            UPDATE SKILL my_skill
            SET
                SoUrCe = 'new_source'
        """
        ast = parse_sql(sql)
        expected_ast = UpdateSkill(
            name=Identifier('my_skill'),
            updated_params={'source': 'new_source'}
        )
        assert ast.to_tree() == expected_ast.to_tree()

    def test_create_agent_case_handling(self):
        sql = """
            CREATE AGENT my_agent
            USING
                MoDeL = 'my_model',
                SkIlLs = ['skill1', 'skill2']
        """
        ast = parse_sql(sql)
        expected_ast = CreateAgent(
            name=Identifier('my_agent'),
            model='my_model',
            params={'skills': ['skill1', 'skill2']}
        )
        assert ast.to_tree() == expected_ast.to_tree()

    def test_update_agent_case_handling(self):
        sql = """
            UPDATE AGENT my_agent
            SET
                MoDeL = 'new_model',
                SkIlLs = ['new_skill1', 'new_skill2']
        """
        ast = parse_sql(sql)
        expected_ast = UpdateAgent(
            name=Identifier('my_agent'),
            updated_params={'model': 'new_model', 'skills': ['new_skill1', 'new_skill2']}
        )
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