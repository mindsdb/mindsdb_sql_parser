from copy import deepcopy

from mindsdb_sql_parser.ast import *


class TestAST:
    def test_copy(self):
        ast = Select(
            targets=[Identifier.from_path_str('col1')],
            from_table=Identifier.from_path_str('tab'),
            where=BinaryOperation(
                op='=',
                args=(
                  Identifier.from_path_str('col3'),
                  Constant(1),
                )
            ),
        )

        ast2 = ast.copy()
        # same tree
        assert ast.to_tree() == ast2.to_tree()
        # not same objects
        assert not ast.to_tree() is ast2.to_tree()

        # change
        ast.where.args[0] = Constant(1)
        assert ast.to_tree() != ast2.to_tree()

    def test_identifier_deepcopy_is_quoted(self):
        ident = Identifier('`a`')
        ident2 = deepcopy(ident)
        assert ident2.is_quoted == [True]

    def test_identifier_to_string(self):
        test_cases = [
            'test',
            'Test',
            'TEST',
            '`test`',
            '`Test`',
            '`TEST`'
        ]

        for test_case in test_cases:
            assert Identifier(test_case).to_string() == test_case

        for i in range(len(test_cases)):
            for test_case in test_cases:
                test_str = f'{test_case}.{test_cases[i]}'
                assert Identifier(test_str).to_string() == test_str
