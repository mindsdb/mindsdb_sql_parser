from mindsdb_sql_parser.ast.base import ASTNode
from mindsdb_sql_parser.utils import indent


class UpdateDatabase(ASTNode):
    def __init__(self, name, updated_params, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.params = updated_params

    def to_tree(self, *args, level=0, **kwargs):
        ind = indent(level)
        out_str = f'{ind}UpdateDatabase(' \
                  f'name={self.name.to_string()}, ' \
                  f'updated_params={self.params})'
        return out_str

    def get_string(self, *args, **kwargs):
        params = self.params.copy()

        set_ar = [f'{k}={repr(v)}' for k, v in params.items()]
        set_str = ', '.join(set_ar)

        out_str = f'UPDATE DATABASE {self.name.to_string()} SET {set_str}'
        return out_str