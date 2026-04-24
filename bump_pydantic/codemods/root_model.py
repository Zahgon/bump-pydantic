from typing import Union

import libcst as cst
from libcst import matchers as m
from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor, RemoveImportsVisitor

# Match BaseModel or pydantic.BaseModel
BASE_MODEL_ARG = m.Arg(value=m.Name("BaseModel") | m.Attribute(value=m.Name("pydantic"), attr=m.Name("BaseModel")))
BASE_MODEL_MATCHER = m.ClassDef(bases=[m.ZeroOrMore(), BASE_MODEL_ARG, m.ZeroOrMore()])
# Match the assignment `__root__ = ...`
ROOT_ASSIGNMENT_MATCHER = m.Assign(targets=[m.AssignTarget(target=m.Name("__root__"))])


class RootModelCommand(VisitorBasedCodemodCommand):
    def __init__(self, context: CodemodContext) -> None:
        raise NotImplementedError

    @m.visit(BASE_MODEL_MATCHER)
    def visit_base_model(self, node: cst.ClassDef) -> None:
        pass

    @m.leave(BASE_MODEL_MATCHER)
    def leave_base_model(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.ClassDef:
        pass

    @m.leave(ROOT_ASSIGNMENT_MATCHER)
    def leave_root_assignment(self, original_node: cst.Assign, updated_node: cst.Assign) -> cst.Assign:
        pass


if __name__ == "__main__":
    import textwrap

    from rich.console import Console

    console = Console()

    source = textwrap.dedent(
        """
        from typing import Any, Dict
        from pydantic import BaseModel, Field

        class A(BaseModel):
            __root__ = Dict[str, Dict[str, Any]]
        """
    )
    console.print(source)
    console.print("=" * 80)

    mod = cst.parse_module(source)

    context = CodemodContext(filename="main.py")
    wrapper = cst.MetadataWrapper(mod)
    command = RootModelCommand(context=context)
    mod = wrapper.visit(command)

    wrapper = cst.MetadataWrapper(mod)
    command = AddImportsVisitor(context=context)  # type: ignore[assignment]
    mod = wrapper.visit(command)

    # wrapper = cst.MetadataWrapper(mod)
    # command = RemoveImportsVisitor(context=context)  # type: ignore[assignment]
    # mod = wrapper.visit(command)
    # console.print(mod.code)
