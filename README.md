# MindsDB SQL Parser 🚧


# Installation

```
  pip install mindsdb_sql_parser
```

## How to use

```python

from mindsdb_sql_parser import parse_sql

query = parse_sql('select b from aaa where c=1')

# result is abstract syntax tree (AST) 
query

# string representation of AST
query.to_tree()

# representation of tree as sql string. it can not exactly match with original sql
query.to_string()

```

## Architecture

For parsing is used [SLY](https://sly.readthedocs.io/en/latest/sly.html) library.

Parsing consists of 2 stages, (separate module for every dialect): 
- Defining keywords in lexer.py module. It is made mostly with regexp 
- Defining syntax rules in parser.py module. It is made by describing rules in [BNF grammar](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form)
  - Syntax is defined in decorator of function. Inside of decorator you can use keyword itself or other function from parser
  - Output of function can be used as input in other functions of parser
  - Outputs of the parser is listed in "Top-level statements". It has to be Abstract syntax tree (AST) object.

SLY does not support inheritance, therefore every dialect is described completely, without extension one from another.  

### [AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree)
- Structure of AST is defined in separate modules (in parser/ast/).
- It can be inherited
- Every class have to have these methods:
  - to_tree - to return hierarchical representation of object
  - get_string - to return object as sql expression (or sub-expression)
  - copy - to copy AST-tree to new object

### Error handling

For better user experience parsing error contains useful information about problem location and possible solution to solve it. 
1. it shows location of error if 
  - character isn't parsed (by lexer)
  - token is unexpected (by parser)
2. it tries to propose correct token instead (or before) error location. Possible options
  - Keyword will be showed as is.
  - '[number]' - if float and integer is expected
  - '[string]' - if string is expected
  - '[identifier]' - if name of the objects is expected. For example, they are bold words here:
    - "select **x** as **name** from **tbl1** where **col**=1"

How suggestion works:
It uses next possible tokens defined by syntax rules.
If this is the end of the query: just shows these tokens.
Else:
- it tries to replace bad token with other token from list of possible tokens
- tries to parse query once again, if there is no error:
  - add this token to suggestion list
- second iteration: put possible token before bad token (instead of replacement) and repeat the same operation.


# How to test

```bash
pip install -r requirements_test.txt
env PYTHONPATH=./ pytest
```
