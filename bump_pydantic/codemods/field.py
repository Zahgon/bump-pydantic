from typing import List, Union

import libcst as cst
from libcst import matchers as m
from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor, RemoveImportsVisitor

RENAMED_KEYWORDS = {
    "min_items": "min_length",
    "max_items": "max_length",
    "allow_mutation": "frozen",
    "example": "examples",
    "regex": "pattern",
    # NOTE: This is only for BaseSettings.
    "env": "validation_alias",
}

IMPORT_FIELD = m.Module(
    body=[
        m.ZeroOrMore(),
        m.SimpleStatementLine(
            body=[
                m.ZeroOrMore(),
                m.ImportFrom(
                    module=m.Name("pydantic"),
                    names=[
                        m.ZeroOrMore(),
                        m.ImportAlias(name=m.Name("Field")),
                        m.ZeroOrMore(),
                    ],
                )
                | m.ImportFrom(
                    module=m.Name("pydantic") | m.Name("pydantic_settings"),
                    names=[
                        m.ZeroOrMore(),
                        m.ImportAlias(name=m.Name("BaseSettings")),
                        m.ZeroOrMore(),
                    ],
                ),
                m.ZeroOrMore(),
            ],
        ),
        m.ZeroOrMore(),
    ]
)

ANN_ASSIGN_WITH_FIELD = m.AnnAssign(
    value=m.Call(func=m.Name("Field")),
) | m.AnnAssign(
    annotation=m.Annotation(
        annotation=m.Subscript(
            slice=[
                m.ZeroOrMore(),
                m.SubscriptElement(slice=m.Index(value=m.Call(func=m.Name("Field")))),
                m.ZeroOrMore(),
            ]
        )
    )
)


class FieldCodemod(VisitorBasedCodemodCommand):
    def __init__(self, context: CodemodContext) -> None:
        raise NotImplementedError

    @m.visit(IMPORT_FIELD)
    def visit_field_import(self, node: cst.Module) -> None:
        pass

    @m.leave(IMPORT_FIELD)
    def leave_field_import(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
        pass

    @m.visit(ANN_ASSIGN_WITH_FIELD)
    def visit_field_assign(self, node: cst.AnnAssign) -> None:
        pass

    @m.leave(ANN_ASSIGN_WITH_FIELD)
    def leave_field_assign(self, original_node: cst.AnnAssign, updated_node: cst.AnnAssign) -> cst.AnnAssign:
        pass

    @m.visit(m.Call(func=m.Name("Field")))
    def visit_field_call(self, node: cst.Call) -> None:
        # Check if there's a `const=True` argument.
        pass

    @m.leave(m.Call(func=m.Name("Field")))
    def leave_field_call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        pass


if __name__ == "__main__":
    import textwrap

    from rich.console import Console

    console = Console()

    source = textwrap.dedent(
        """
        from typing import Annotated

        from pydantic import BaseModel, Field

        class A(BaseModel):
            a: Annotated[List[str], Field(..., description="My description", min_items=1)]
        """
    )
    console.print(source)
    console.print("=" * 80)

    mod = cst.parse_module(source)
    context = CodemodContext(filename="main.py")
    wrapper = cst.MetadataWrapper(mod)
    command = FieldCodemod(context=context)
    console.print(mod)

    mod = wrapper.visit(command)
    wrapper = cst.MetadataWrapper(mod)
    command = AddImportsVisitor(context=context)  # type: ignore[assignment]
    mod = wrapper.visit(command)
    console.print(mod.code)
