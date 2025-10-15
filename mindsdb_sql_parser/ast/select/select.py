from typing import List, Union
from mindsdb_sql_parser.ast.base import ASTNode
from mindsdb_sql_parser.utils import indent, dump_json
from mindsdb_sql_parser.ast.select.operation import Object


class Select(ASTNode):

    def __init__(self,
                 targets,
                 distinct: Union[List, bool] = False,
                 from_table=None,
                 where=None,
                 group_by=None,
                 having=None,
                 order_by=None,
                 limit=None,
                 offset=None,
                 cte=None,
                 mode=None,
                 modifiers=None,
                 using=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.targets = targets

        # if it is list: SELECT DISTINCT ON (c1, c2) ...
        self.distinct = distinct
        self.from_table = from_table
        self.where = where
        self.group_by = group_by
        self.having = having
        self.order_by = order_by
        self.limit = limit
        self.offset = offset
        self.cte = cte
        self.mode = mode
        if modifiers is None:
            modifiers = []
        self.modifiers = modifiers
        self.using = using

        if self.alias:
            self.parentheses = True

    def to_tree(self, *args, level=0, **kwargs):
        ind = indent(level)
        ind1 = indent(level+1)

        cte_str = ''
        if self.cte:
            cte_trees = ',\n'.join([t.to_tree(level=level + 2) for t in self.cte])
            cte_str = f'\n{ind1}cte=[\n{cte_trees}\n{ind1}],'

        alias_str = f'\n{ind1}alias={self.alias.to_tree()},' if self.alias else ''
        distinct_str = f'\n{ind1}distinct={repr(self.distinct)},' if self.distinct else ''
        parentheses_str = f'\n{ind1}parentheses={repr(self.parentheses)},' if self.parentheses else ''

        target_trees = ',\n'.join([t.to_tree(level=level+2) for t in self.targets])
        targets_str = f'\n{ind1}targets=[\n{target_trees}\n{ind1}],'

        from_str = f'\n{ind1}from_table=\n{self.from_table.to_tree(level=level+2)},' if self.from_table else ''
        where_str = f'\n{ind1}where=\n{self.where.to_tree(level=level+2)},' if self.where else ''

        group_by_str = ''
        if self.group_by:
            group_by_trees = ',\n'.join([t.to_tree(level=level+2) for t in self.group_by])
            group_by_str = f'\n{ind1}group_by=[\n{group_by_trees}\n{ind1}],'

        having_str = f'\n{ind1}having=\n{self.having.to_tree(level=level+2)},' if self.having else ''

        order_by_str = ''
        if self.order_by:
            order_by_trees = ',\n'.join([t.to_tree(level=level + 2) for t in self.order_by])
            order_by_str = f'\n{ind1}order_by=[\n{order_by_trees}\n{ind1}],'
        limit_str = f'\n{ind1}limit={self.limit.to_tree(level=0)},' if self.limit else ''
        offset_str = f'\n{ind1}offset={self.offset.to_tree(level=0)},' if self.offset else ''
        mode_str = f'\n{ind1}mode={self.mode},' if self.mode else ''

        using_str = ''
        if self.using:
            using_str = f'\n{ind1}using={repr(self.using)},'

        out_str = f'{ind}Select(' \
                  f'{cte_str}' \
                  f'{alias_str}' \
                  f'{distinct_str}' \
                  f'{parentheses_str}' \
                  f'{targets_str}' \
                  f'{from_str}' \
                  f'{where_str}' \
                  f'{group_by_str}' \
                  f'{having_str}' \
                  f'{order_by_str}' \
                  f'{limit_str}' \
                  f'{offset_str}' \
                  f'{mode_str}' \
                  f'{using_str}' \
                  f'\n{ind})'
        return out_str

    def get_string(self, *args, **kwargs):
        from mindsdb_sql_parser.ast.select.identifier import Identifier
        out_str = ''
        if self.cte is not None:
            cte_str = ', '.join([out.to_string() for out in self.cte])
            out_str += f'WITH {cte_str} '

        out_str += "SELECT"

        if self.distinct is True:
            out_str += ' DISTINCT'
        elif isinstance(self.distinct, list):
            distinct_str = ', '.join([c.to_string() for c in self.distinct])

            out_str += f' DISTINCT ON ({distinct_str})'

        targets_str = ', '.join([out.to_string() for out in self.targets])
        out_str += f' {targets_str}'

        if self.from_table is not None:
            from_table_str = str(self.from_table)
            out_str += f' FROM {from_table_str}'

        if self.where is not None:
            out_str += f' WHERE {self.where.to_string()}'

        if self.group_by is not None:
            parts = []
            for item in self.group_by:
                part = item.to_string()
                if isinstance(item, Identifier) and item.with_rollup:
                    part += ' WITH ROLLUP'
                parts.append(part)
            group_by_str = ', '.join(parts)
            out_str += f' GROUP BY {group_by_str}'

        if self.having is not None:
            having_str = str(self.having)
            out_str += f' HAVING {having_str}'

        if self.order_by is not None:
            order_by_str = ', '.join([out.to_string() for out in self.order_by])
            out_str += f' ORDER BY {order_by_str}'

        if self.limit is not None:
            out_str += f' LIMIT {self.limit.to_string()}'

        if self.offset is not None:
            out_str += f' OFFSET {self.offset.to_string()}'

        if self.mode is not None:
            out_str += f' {self.mode}'

        if self.using:

            using_ar = []
            for key, value in self.using.items():
                if isinstance(value, Object):
                    args = [
                        f'{k}={dump_json(v)}'
                        for k, v in value.params.items()
                    ]
                    args_str = ', '.join(args)
                    value = f'{value.type}({args_str})'
                if isinstance(value, Identifier):
                    value = value.to_string()
                else:
                    value = dump_json(value)

                using_ar.append(f'{Identifier(key).to_string()}={value}')

            out_str += f' USING ' + ', '.join(using_ar)

        return out_str

