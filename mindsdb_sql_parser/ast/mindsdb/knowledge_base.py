from mindsdb_sql_parser.ast.base import ASTNode
from mindsdb_sql_parser.ast import Identifier
from mindsdb_sql_parser.utils import indent


class CreateKnowledgeBase(ASTNode):
    """
    Create a new knowledge base
    """
    def __init__(
        self,
        name,
        model=None,
        storage=None,
        from_select=None,
        params=None,
        if_not_exists=False,
        *args,
        **kwargs,
    ):
        """
        Args:
            name: Identifier -- name of the knowledge base
            model: Identifier -- name of the model to use
            storage: Identifier -- name of the storage to use
            from_select: SelectStatement -- select statement to use as the source of the knowledge base
            params: dict -- additional parameters to pass to the knowledge base. E.g., chunking strategy, etc.
            if_not_exists: bool -- if True, do not raise an error if the knowledge base already exists
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self.model = model
        self.storage = storage
        self.params = params
        self.if_not_exists = if_not_exists
        self.from_query = from_select

    def to_tree(self, *args, level=0, **kwargs):
        ind = indent(level)
        storage_str = f"{ind}  storage={self.storage.to_string()},\n" if self.storage else ""
        model_str = f"{ind}  model={self.model.to_string()},\n" if self.model else ""
        out_str = f"{ind}CreateKnowledgeBase(\n" \
        f"{ind}  if_not_exists={self.if_not_exists},\n" \
        f"{ind}  name={self.name.to_string()},\n" \
        f"{ind}  from_query={self.from_query.to_tree(level=level + 1) if self.from_query else None},\n" \
        f"{ind}{model_str}{storage_str}{ind}  params={self.params}\n" \
        f"{ind})"

        return out_str

    def get_string(self, *args, **kwargs):
        from_query_str = (
            f"FROM ({self.from_query.get_string()})" if self.from_query else ""
        )

        using_ar = []
        if self.storage:
            using_ar.append(f"  STORAGE={self.storage.to_string()}")
        if self.model:
            using_ar.append(f"  MODEL={self.model.to_string()}")

        params = self.params.copy()
        if params:
            using_ar += [f"{k}={repr(v)}" for k, v in params.items()]
        if using_ar:
            using_str = "USING " + ", ".join(using_ar)
        else:
            using_str = ""

        out_str = (
            f"CREATE KNOWLEDGE_BASE {'IF NOT EXISTS ' if self.if_not_exists else ''}{self.name.to_string()} "
            f"{from_query_str} "
            f"{using_str}"
        )

        return out_str

    def __repr__(self) -> str:
        return self.to_tree()


class AlterKnowledgeBase(ASTNode):
    """
    Update the knowledge base
    """
    def __init__(
        self,
        name,
        params=None,
        *args,
        **kwargs,
    ):
        """
        Args:
            name: Identifier -- name of the knowledge base
            params: dict -- additional parameters to pass to the knowledge base. E.g., chunking strategy, etc.
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self.params = params
    def to_tree(self, *args, level=0, **kwargs):
        ind = indent(level)
        out_str = f"{ind}AlterKnowledgeBase(\n" \
        f"{ind}  name={self.name.to_string()},\n" \
        f"{ind}  params={self.params}\n" \
        f"{ind})"
        return out_str

    def get_string(self, *args, **kwargs):

        using_ar = []
        params = self.params.copy()
        if params:
            using_ar += [f"{k}={repr(v)}" for k, v in params.items()]
        if using_ar:
            using_str = "USING " + ", ".join(using_ar)
        else:
            using_str = ""

        out_str = (
            f"ALTER KNOWLEDGE_BASE {self.name.to_string()} "
            f"{using_str}"
        )

        return out_str

    def __repr__(self) -> str:
        return self.to_tree()


class DropKnowledgeBase(ASTNode):
    """
    Delete a knowledge base
    """
    def __init__(self, name, if_exists=False, *args, **kwargs):
        """
        Args:
            name: Identifier -- name of the knowledge base
            if_exists: bool -- if True, do not raise an error if the knowledge base does not exist
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self.if_exists = if_exists

    def to_tree(self, *args, level=0, **kwargs):
        ind = indent(level)
        out_str = (
            f"{ind}DropKnowledgeBase("
            f"{ind}    if_exists={self.if_exists},"
            f"name={self.name.to_string()})"
        )
        return out_str

    def get_string(self, *args, **kwargs):
        out_str = f'DROP KNOWLEDGE_BASE {"IF EXISTS " if self.if_exists else ""}{self.name.to_string()}'
        return out_str


class CreateKnowledgeBaseIndex(ASTNode):
    """
    Create a new index in the knowledge base
    """
    def __init__(self, name, *args, **kwargs):
        """
        Args:
            name: Identifier -- name of the knowledge base
        """
        super().__init__(*args, **kwargs)
        self.name = name

    def to_tree(self, *args, level=0, **kwargs):
        ind = indent(level)
        out_str = f"{ind}CreateKnowledgeBaseIndex(name={self.name.to_string()})"
        return out_str

    def get_string(self, *args, **kwargs):
        out_str = f'CREATE INDEX ON KNOWLEDGE_BASE {self.name.to_string()}'
        return out_str


class DropKnowledgeBaseIndex(ASTNode):
    """
    Delete an index in the knowledge base
    """
    def __init__(self, name, *args, **kwargs):
        """
        Args:
            name: Identifier -- name of the knowledge base
        """
        super().__init__(*args, **kwargs)
        self.name = name

    def to_tree(self, *args, level=0, **kwargs):
        ind = indent(level)
        out_str = f"{ind}DropKnowledgeBaseIndex(name={self.name.to_string()})"
        return out_str

    def get_string(self, *args, **kwargs):
        out_str = f'DROP INDEX ON KNOWLEDGE_BASE {self.name.to_string()}'
        return out_str


class EvaluateKnowledgeBase(ASTNode):
    """
    Evaluate a knowledge base.
    """
    def __init__(self, name: Identifier, params: dict = None, *args, **kwargs):
        """
        Args:
            name: Identifier -- name of the knowledge base to evaluate.
            params: dict -- parameters to pass to the evaluation.
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self.params = params if params is not None else {}

    def to_tree(self, *args, level=0, **kwargs):
        ind = indent(level)

        param_str = ""
        if self.params:
            param_items = []
            for k, v in self.params.items():
                if isinstance(v, Identifier):
                    param_items.append(f"{ind}    {k}={v.to_string()}")
                else:
                    param_items.append(f"{ind}    {k}={repr(v)}")
            param_str = ",\n".join(param_items)

        output_str = (
            f"{ind}EvaluateKnowledgeBase(\n"
            f"{ind}    name={self.name.to_string()},\n"
            f"{param_str}\n"
            f"{ind})"
        )

        return output_str

    def get_string(self, *args, **kwargs):
        using_str = ""

        if self.params:
            using_args = []
            for k, v in self.params.items():
                if isinstance(v, Identifier):
                    using_args.append(f"{k}={v.to_string()}")
                else:
                    using_args.append(f"{k}={repr(v)}")

            using_str = "USING " + ", ".join(using_args)

        output_str = (
            f"EVALUATE KNOWLEDGE_BASE {self.name.to_string()} "
            f"{using_str}"
        )

        return output_str.strip()
