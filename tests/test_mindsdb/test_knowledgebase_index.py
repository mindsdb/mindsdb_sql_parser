from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast.mindsdb.knowledge_base import CreateKnowledgeBaseIndex, DropKnowledgeBaseIndex
from mindsdb_sql_parser.ast import *

class TestKB:

    def test_create_knowledge_base_index(self):
        # create without select

        sql = """CREATE INDEX ON KNOWLEDGE_BASE my_kb"""
        ast = parse_sql(sql)
        print(ast)
        expected_ast = CreateKnowledgeBaseIndex(
            name=Identifier('my_kb'),
        )
        assert str(ast).lower() == sql.lower()
        assert ast.to_tree() == expected_ast.to_tree()

    def test_drop_knowledge_base_index(self):
        # create without select

        sql = """DROP INDEX ON KNOWLEDGE_BASE my_kb"""
        ast = parse_sql(sql)
        print(ast)
        expected_ast = DropKnowledgeBaseIndex(
            name=Identifier('my_kb'),
        )
        assert ast.to_tree() == expected_ast.to_tree()

