from mindsdb_sql_parser.exceptions import ParsingException


def indent(level):
    return '  ' * level


def ensure_select_keyword_order(select, operation):
    op_to_attr = {
        'FROM': select.from_table,
        'WHERE': select.where,
        'GROUP BY': select.group_by,
        'HAVING': select.having,
        'ORDER BY': select.order_by,
        'LIMIT': select.limit,
        'OFFSET': select.offset,
        'MODE': select.mode,
    }

    requirements = {
        'WHERE': ['FROM'],
        'GROUP BY': ['FROM'],
        'ORDER BY': ['FROM'],
        # 'HAVING': ['GROUP BY'],
    }

    precedence = ['FROM', 'WHERE', 'GROUP BY', 'HAVING', 'ORDER BY', 'LIMIT', 'OFFSET', 'MODE']

    if op_to_attr[operation]:
        raise ParsingException(f"Duplicate {operation} clause. Only one {operation} allowed per SELECT.")

    op_requires = requirements.get(operation, [])

    for req in op_requires:
        if not op_to_attr[req]:
            raise ParsingException(f"{operation} requires {req}")

    op_precedence_pos = precedence.index(operation)

    for next_op in precedence[op_precedence_pos:]:
        if op_to_attr[next_op]:
            raise ParsingException(f"{operation} must go before {next_op}")


class JoinType:
    JOIN = 'JOIN'
    INNER_JOIN = 'INNER JOIN'
    OUTER_JOIN = 'OUTER JOIN'
    CROSS_JOIN = 'CROSS JOIN'
    LEFT_JOIN = 'LEFT JOIN'
    RIGHT_JOIN = 'RIGHT JOIN'
    FULL_JOIN = 'FULL JOIN'


def to_single_line(text):
    text = '\t'.join([line.strip() for line in text.split('\n')])
    text = text.replace('\t', ' ')
    text = ' '.join(text.split())
    return text


def tokens_to_string(tokens):
    # converts list of token (after lexer) to original string

    line_num = tokens[0].lineno
    shift = tokens[0].index
    last_pos = 0
    content, line = '', ''

    for token in tokens:
        if token.lineno != line_num:
            # go to new line
            content += line + '\n'
            line = ''
            line_num = token.lineno

            # because sly parser store only absolute position index:
            #   memorizing last token index to shift next lne
            shift = last_pos + 1

        # filling space between tokens
        line += ' '*(token.index - shift - len(line))

        # add token
        line += token.value

        last_pos = token.index + len(token.value)

    # last line
    content += line
    return content


def unquote(s, is_double_quoted=False):
    s = s.replace('\\"', '"').replace("\\'", "'")
    if is_double_quoted:
        s = s.replace('""', '"')
    else:
        s = s.replace("''", "'")
    return s


def dump_json(obj) -> str:
    '''
       dump dict into json-like string using:
       - single quotes for strings
       - the same quoting rules as `unquote` function
    '''


    if isinstance(obj, dict):
        items = []
        for k, v in obj.items():
            # keys must be strings in JSON
            if not isinstance(k, str):
                k = str(k)
            items.append(f'{dump_json(k)}: {dump_json(v)}')
        return "{" + ", ".join(items) + "}"

    if isinstance(obj, (list, tuple)):
        items = [
            dump_json(i) for i in obj
        ]
        return "[" + ", ".join(items) + "]"

    if isinstance(obj, str):
        obj = obj.replace("'", "''")
        return f"'{obj}'"

    if isinstance(obj, (int, float)):
        if obj != obj:  # NaN
            return "null"
        if obj == float('inf'):
            return "null"
        if obj == float('-inf'):
            return "null"
        return str(obj)

    if obj is None:
        return "null"

    if isinstance(obj, bool):
        return "true" if obj else "false"

    return dump_json(str(obj))
