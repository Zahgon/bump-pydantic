from typing import cast

import libcst as cst
from libcst import matchers as m
from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor, RemoveImportsVisitor

CONSTR_CALL = m.Call(func=m.Name("constr") | m.Attribute(value=m.Name("pydantic"), attr=m.Name("constr")))
CON_NUMBER_CALL = m.OneOf(
    *[
        m.Call(func=m.Name(name) | m.Attribute(value=m.Name("pydantic"), attr=m.Name(name)))
        for name in ("conint", "confloat", "condecimal", "conbytes")
    ]
)
CON_COLLECTION_CALL = m.OneOf(
    *[
        m.Call(func=m.Name(name) | m.Attribute(value=m.Name("pydantic"), attr=m.Name(name)))
        for name in ("conlist", "conset", "confrozenset")
    ]
)

MAP_FUNC_TO_TYPE = {
    "constr": "str",
    "conint": "int",
    "confloat": "float",
    "condecimal": "Decimal",
    "conbytes": "bytes",
    "conlist": "List",
    "conset": "Set",
    "confrozenset": "FrozenSet",
}
MAP_TYPE_TO_NEEDED_IMPORT = {
    "Decimal": {"module": "decimal", "obj": "Decimal"},
    "List": {"module": "typing", "obj": "List"},
    "Set": {"module": "typing", "obj": "Set"},
    "FrozenSet": {"module": "typing", "obj": "FrozenSet"},
}
COLLECTIONS = ("List", "Set", "FrozenSet")


class ConFuncCallCommand(VisitorBasedCodemodCommand):
    def __init__(self, context: CodemodContext) -> None:
        raise NotImplementedError

    @m.leave(CON_NUMBER_CALL | CON_COLLECTION_CALL | CONSTR_CALL)
    def leave_annotation_call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Subscript:
        pass

    @m.leave(CONSTR_CALL)
    def leave_constr_call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        pass

    @m.leave(CON_NUMBER_CALL)
    def leave_con_number_call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        pass

    @m.leave(CON_COLLECTION_CALL)
    def leave_con_collection_call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        pass

    def _remove_import(self, func: cst.BaseExpression) -> None:
        pass


if __name__ == "__main__":
    import textwrap

    from rich.console import Console

    console = Console()

    source = textwrap.dedent(
        """
        from pydantic import BaseModel, constr

        class A(BaseModel):
            a: constr(max_length=10)
            b: conint(ge=0, le=100)
            c: confloat(ge=0, le=100)
            d: condecimal(ge=0, le=100)
            e: conbytes(max_length=10)
            f: conlist(int, min_items=1, max_items=10)
            g: conset(float, min_items=1, max_items=10)
            h: confrozenset(str, min_items=1, max_items=10)
            i: conlist(int, unique_items=True)
        """
    )
    console.print(source)
    console.print("=" * 80)

    mod = cst.parse_module(source)
    context = CodemodContext(filename="main.py")
    wrapper = cst.MetadataWrapper(mod)
    command = ConFuncCallCommand(context=context)
    console.print(mod)

    mod = wrapper.visit(command)
    print(mod.code)
