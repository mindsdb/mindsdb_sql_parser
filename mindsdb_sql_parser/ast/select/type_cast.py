from mindsdb_sql_parser.ast.base import ASTNode
from mindsdb_sql_parser.utils import indent


class TypeCast(ASTNode):
    def __init__(self, type_name, arg, precision=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type_name = type_name
        self.arg = arg
        self.precision = precision

    def to_tree(self, *args, level=0, **kwargs):
        out_str = indent(level) + f'TypeCast(type_name={repr(self.type_name)}, precision={self.precision}, arg=\n{indent(level+1)}{self.arg.to_tree()})'
        return out_str

    def get_string(self, *args, **kwargs):
        type_name = self.type_name
        if self.precision is not None:
            precision = map(str, self.precision)
            type_name += f'({",".join(precision)})'
        return f'CAST({str(self.arg)} AS {type_name})'
