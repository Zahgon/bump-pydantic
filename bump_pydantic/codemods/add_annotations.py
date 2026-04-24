from __future__ import annotations

import libcst as cst
import libcst.matchers as m
from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand
from libcst.metadata import FullyQualifiedNameProvider, QualifiedName

from bump_pydantic.codemods.class_def_visitor import ClassDefVisitor

COMMENT = "# TODO[pydantic]: add type annotation"


class AddAnnotationsCommand(VisitorBasedCodemodCommand):
    """This codemod adds a type annotation or TODO comment to pydantic fields without
    a type annotation.

    Example::
        # Before
        ```py
        from pydantic import BaseModel, Field

        class Foo(BaseModel):
            name: str
            is_sale = True
            tags = ["tag1", "tag2"]
            price = 10.5
            description = "Some item"
            active = Field(default=True)
            ready = Field(True)
            age = Field(10, title="Age")
        ```

        # After
        ```py
        from pydantic import BaseModel, Field

        class Foo(BaseModel):
            name: str
            is_sale: bool = True
            # TODO[pydantic]: add type annotation
            tags = ["tag1", "tag2"]
            price: float = 10.5
            description: str = "Some item"
            active: bool = Field(default=True)
            ready: bool = Field(True)
            age: int = Field(10, title="Age")
        ```
    """

    METADATA_DEPENDENCIES = (FullyQualifiedNameProvider,)

    def __init__(self, context: CodemodContext) -> None:
        raise NotImplementedError

    def visit_ClassDef(self, node: cst.ClassDef) -> None:
        pass

    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.ClassDef:
        pass

    def visit_SimpleStatementLine(self, node: cst.SimpleStatementLine) -> None:
        pass

    def leave_SimpleStatementLine(
        self, original_node: cst.SimpleStatementLine, updated_node: cst.SimpleStatementLine
    ) -> cst.SimpleStatementLine:
        pass

    def leave_Assign(self, original_node: cst.Assign, updated_node: cst.Assign) -> cst.Assign | cst.AnnAssign:
        pass
