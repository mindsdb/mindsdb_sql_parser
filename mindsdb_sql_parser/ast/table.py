from typing import Optional, List, Any

from mindsdb_sql_parser.ast.base import ASTNode


class Table(ASTNode):
    """AST node representing a TABLE statement with optional ORDER BY, LIMIT, and OFFSET clauses.
    https://dev.mysql.com/doc/refman/8.4/en/table.html

    Args:
        name: The name of the table (Identifier).
        order_by: Optional list of ORDER BY terms.
        limit: Optional LIMIT value (Constant).
        offset: Optional OFFSET value (Constant).
        *args: Additional positional arguments for ASTNode.
        **kwargs: Additional keyword arguments for ASTNode.
    """
    def __init__(
        self,
        name: Any,
        order_by: Optional[List[Any]] = None,
        limit: Optional[Any] = None,
        offset: Optional[Any] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.name = name
        self.order_by = order_by
        self.limit = limit
        self.offset = offset

    def to_tree(self, *args, level: int = 0, **kwargs) -> str:
        """Returns a string representation of the AST tree for this node.

        Args:
            level: Indentation level for pretty printing.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The tree representation of the node.
        """
        ind = '  ' * level
        out = f'{ind}Table(\n'
        out += f'{ind}  name={self.name},\n'
        if self.order_by:
            out += f'{ind}  order_by={self.order_by},\n'
        if self.limit:
            out += f'{ind}  limit={self.limit},\n'
        if self.offset:
            out += f'{ind}  offset={self.offset},\n'
        out += f'{ind})'
        return out

    def to_string(self, *args, **kwargs) -> str:
        """Returns a SQL string representation of the TABLE statement.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The SQL string representation.
        """
        s = f'TABLE {self.name}'
        if self.order_by:
            s += ' ORDER BY ' + ', '.join([o.to_string() for o in self.order_by])
        if self.limit:
            s += f' LIMIT {self.limit.to_string()}'
        if self.offset:
            s += f' OFFSET {self.offset.to_string()}'
        return s
