from typing import List

import libcst as cst
from libcst import matchers as m
from libcst._nodes.module import Module
from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor, RemoveImportsVisitor

PREFIX_COMMENT = "# TODO[pydantic]: "
REFACTOR_COMMENT = (
    f"{PREFIX_COMMENT}We couldn't refactor the `{{old_name}}`, please replace it by `{{new_name}}` manually."
)
VALIDATOR_COMMENT = REFACTOR_COMMENT.format(old_name="validator", new_name="field_validator")
ROOT_VALIDATOR_COMMENT = REFACTOR_COMMENT.format(old_name="root_validator", new_name="model_validator")
CHECK_LINK_COMMENT = "# Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-validators for more information."

IMPORT_VALIDATOR = m.Module(
    body=[
        m.ZeroOrMore(),
        m.SimpleStatementLine(
            body=[
                m.ZeroOrMore(),
                m.ImportFrom(
                    module=m.Name("pydantic"),
                    names=[
                        m.ZeroOrMore(),
                        m.ImportAlias(name=m.Name("validator")),
                        m.ZeroOrMore(),
                    ],
                ),
                m.ZeroOrMore(),
            ],
        ),
        m.ZeroOrMore(),
    ]
)
VALIDATOR_DECORATOR = m.Decorator(decorator=m.Call(func=m.Name("validator")))
VALIDATOR_FUNCTION = m.FunctionDef(decorators=[m.ZeroOrMore(), VALIDATOR_DECORATOR, m.ZeroOrMore()])

IMPORT_ROOT_VALIDATOR = m.Module(
    body=[
        m.ZeroOrMore(),
        m.SimpleStatementLine(
            body=[
                m.ZeroOrMore(),
                m.ImportFrom(
                    module=m.Name("pydantic"),
                    names=[
                        m.ZeroOrMore(),
                        m.ImportAlias(name=m.Name("root_validator")),
                        m.ZeroOrMore(),
                    ],
                ),
                m.ZeroOrMore(),
            ],
        ),
        m.ZeroOrMore(),
    ]
)
ROOT_VALIDATOR_DECORATOR = m.Decorator(decorator=m.Call(func=m.Name("root_validator")))
ROOT_VALIDATOR_FUNCTION = m.FunctionDef(decorators=[m.ZeroOrMore(), ROOT_VALIDATOR_DECORATOR, m.ZeroOrMore()])


class ValidatorCodemod(VisitorBasedCodemodCommand):
    def __init__(self, context: CodemodContext) -> None:
        super().__init__(context)

        self._import_pydantic_validator = self._import_pydantic_root_validator = False
        self._already_modified = False
        self._should_add_comment = False
        self._has_comment = False
        self._args: List[cst.Arg] = []

    @m.visit(IMPORT_VALIDATOR)
    def visit_import_validator(self, node: cst.CSTNode) -> None:
        pass

    def leave_Module(self, original_node: Module, updated_node: Module) -> Module:
        pass

    @m.visit(VALIDATOR_DECORATOR | ROOT_VALIDATOR_DECORATOR)
    def visit_validator_decorator(self, node: cst.Decorator) -> None:
        pass

    @m.visit(VALIDATOR_FUNCTION)
    def visit_validator_func(self, node: cst.FunctionDef) -> None:
        pass

    @m.leave(ROOT_VALIDATOR_DECORATOR)
    def leave_root_validator_func(self, original_node: cst.Decorator, updated_node: cst.Decorator) -> cst.Decorator:
        pass

    @m.leave(VALIDATOR_DECORATOR)
    def leave_validator_decorator(self, original_node: cst.Decorator, updated_node: cst.Decorator) -> cst.Decorator:
        pass

    @m.leave(VALIDATOR_FUNCTION | ROOT_VALIDATOR_FUNCTION)
    def leave_validator_func(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.FunctionDef:
        pass

    def _decorator_with_leading_comment(self, node: cst.Decorator, comment: str) -> cst.Decorator:
        pass

    def _replace_validators(self, node: cst.Decorator, old_name: str, new_name: str) -> cst.Decorator:
        pass


if __name__ == "__main__":
    import textwrap

    from rich.console import Console

    console = Console()

    source = textwrap.dedent(
        """
        from pydantic import BaseModel, validator

        class Foo(BaseModel):
            bar: str

            @validator("bar", pre=True, always=True)
            def bar_validator(cls, v):
                return v
        """
    )
    console.print(source)
    console.print("=" * 80)

    mod = cst.parse_module(source)
    context = CodemodContext(filename="main.py")
    wrapper = cst.MetadataWrapper(mod)
    command = ValidatorCodemod(context=context)
    # console.print(mod)

    mod = wrapper.visit(command)
    wrapper = cst.MetadataWrapper(mod)
    command = AddImportsVisitor(context=context)  # type: ignore[assignment]
    mod = wrapper.visit(command)
    console.print(mod.code)
