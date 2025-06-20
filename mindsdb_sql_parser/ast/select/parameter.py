from mindsdb_sql_parser.ast.base import ASTNode
from mindsdb_sql_parser.utils import indent


class Parameter(ASTNode):
    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value

    def to_tree(self, *args, level=0, **kwargs):
        alias_str = f', alias={self.alias.to_tree()}' if self.alias else ''
        return indent(level) + f'Parameter(value={repr(self.value)}{alias_str})'

    def get_string(self, *args, **kwargs):
        if self.value == '?':
            return self.value
        return ':' + str(self.value)

    def __repr__(self):
        return f'Parameter({repr(self.value)})'