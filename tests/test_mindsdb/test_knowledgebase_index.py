from mindsdb_sql_parser import parse_sql


class TestKB:

    def test_create_knowledge_base_index(self):
        # create without select
        sql = """
            CREATE INDEX ON KNOWLEDGE_BASE my_knowledge_base;
        """
        ast = parse_sql(sql)
        print(ast)
