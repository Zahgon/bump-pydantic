import difflib
import functools
import multiprocessing
import os
import platform
import time
import traceback
from collections import deque
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple, Type, TypeVar, Union

import libcst as cst
from libcst.codemod import CodemodContext, ContextAwareTransformer
from libcst.helpers import calculate_module_and_package
from libcst.metadata import FullRepoManager, FullyQualifiedNameProvider, ScopeProvider
from rich.console import Console
from rich.progress import Progress
from typer import Argument, Exit, Option, Typer, echo
from typing_extensions import ParamSpec

from bump_pydantic import __version__
from bump_pydantic.codemods import Rule, gather_codemods
from bump_pydantic.codemods.class_def_visitor import ClassDefVisitor
from bump_pydantic.glob_helpers import match_glob

app = Typer(invoke_without_command=True, add_completion=False)

entrypoint = functools.partial(app, windows_expand_args=False)

P = ParamSpec("P")
T = TypeVar("T")

DEFAULT_IGNORES = [".venv/**", ".tox/**"]

processes = os.cpu_count()
# Windows has a limit of 61 processes. See https://github.com/python/cpython/issues/89240.
if platform.system() == "Windows" and processes is not None:
    processes = min(processes, 61)


def version_callback(value: bool):
    pass


@app.callback()
def main(
    path: Path = Argument(..., exists=True, dir_okay=True, allow_dash=False),
    disable: List[Rule] = Option(default=[], help="Disable a rule."),
    diff: bool = Option(False, help="Show diff instead of applying changes."),
    ignore: List[str] = Option(default=DEFAULT_IGNORES, help="Ignore a path glob pattern."),
    log_file: Path = Option("log.txt", help="Log errors to this file."),
    version: bool = Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
):
    """Convert Pydantic from V1 to V2 ♻️

    Check the README for more information: https://github.com/pydantic/bump-pydantic.
    """
    pass


def run_codemods(
    codemods: List[Type[ContextAwareTransformer]],
    metadata_manager: FullRepoManager,
    scratch: Dict[str, Any],
    package: Path,
    diff: bool,
    filename: str,
) -> Tuple[Union[str, None], Union[List[str], None]]:
    pass


def color_diff(console: Console, lines: Iterable[str]) -> None:
    pass
