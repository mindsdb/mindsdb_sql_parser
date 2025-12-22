from mindsdb_sql_parser.ast.base import ASTNode
from mindsdb_sql_parser.utils import indent, dump_using_dict


class CreateView(ASTNode):
    def __init__(self,
                 name,
                 query_str,
                 from_table=None,
                 if_not_exists=False,
                 using=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.query_str = query_str
        self.from_table = from_table
        self.if_not_exists = if_not_exists
        self.using = using

    def to_tree(self, *args, level=0, **kwargs):
        ind = indent(level)
        ind1 = indent(level+1)
        name_str = f'\n{ind1}name={self.name.to_string()},'
        from_table_str = f'\n{ind1}from_table=\n{self.from_table.to_tree(level=level+2)},' if self.from_table else ''
        query_str = f'\n{ind1}query="{self.query_str}"'
        if_not_exists_str = f'\n{ind1}if_not_exists=True,' if self.if_not_exists else ''
        using_str = f'\n{ind1}using={self.using},' if self.using else ''

        out_str = f'{ind}CreateView(' \
                  f'{if_not_exists_str}' \
                  f'{name_str}' \
                  f'{query_str}' \
                  f'{from_table_str}' \
                  f'{using_str}' \
                  f'\n{ind})'
        return out_str

    def get_string(self, *args, **kwargs):
        from_str = f'FROM {str(self.from_table)} ' if self.from_table else ''
        using_str = ''
        if self.using:
            using_str = f'USING {dump_using_dict(self.using)}'

        out_str = f'CREATE VIEW {"IF NOT EXISTS " if self.if_not_exists else ""}{self.name.to_string()} {from_str}AS ( {self.query_str} ){using_str}'

        return out_str

