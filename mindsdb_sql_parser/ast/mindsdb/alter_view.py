from mindsdb_sql_parser.ast.base import ASTNode
from mindsdb_sql_parser.utils import indent
from mindsdb_sql_parser.ast.select.identifier import Identifier


class AlterView(ASTNode):
    """
    Alter a view.
    """
    def __init__(
        self,
        name: Identifier,
        query_str: str,
        from_table: Identifier = None,
        *args, 
        **kwargs
    ):
        """
        Args:
            name: Identifier -- name of the view to alter.
            query_str: str -- the new query string for the view.
            from_table: Identifier -- optional table to alter the view from.
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self.query_str = query_str
        self.from_table = from_table

    def to_tree(self, *args, level=0, **kwargs):
        ind = indent(level)
        ind1 = indent(level+1)

        name_str = f'\n{ind1}name={self.name.to_string()},'
        from_table_str = f'\n{ind1}from_table=\n{self.from_table.to_tree(level=level+2)},' if self.from_table else ''
        query_str = f'\n{ind1}query="{self.query_str}"'

        out_str = f'{ind}AlterView(' \
                  f'{name_str}' \
                  f'{query_str}' \
                  f'{from_table_str}' \
                  f'\n{ind})'
        return out_str
    
    def get_string(self, *args, **kwargs):
        from_str = f' FROM {str(self.from_table)}' if self.from_table else ''

        out_str = f'ALTER VIEW {self.name.to_string()}{from_str} AS ( {self.query_str} )'

        return out_str