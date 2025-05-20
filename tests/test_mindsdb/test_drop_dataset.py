from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast.mindsdb import *
from mindsdb_sql_parser.ast import *
from mindsdb_sql_parser.utils import to_single_line  # Added import

class TestDropDataset:
    def test_drop_dataset(self):
        sql = "DROP DATASET IF EXISTS dsname"
        ast = parse_sql(sql)
        expected_ast = DropDataset(name=Identifier('dsname'), if_exists=True)
        assert to_single_line(str(ast)) == to_single_line(sql)  # Standardized
        assert to_single_line(str(ast)) == to_single_line(str(expected_ast))  # Standardized
        assert ast.to_tree() == expected_ast.to_tree()