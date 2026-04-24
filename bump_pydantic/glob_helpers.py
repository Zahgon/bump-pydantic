import fnmatch
import re
from pathlib import Path
from typing import List

MATCH_SEP = r"(?:/|\\)"
MATCH_SEP_OR_END = r"(?:/|\\|\Z)"
MATCH_NON_RECURSIVE = r"[^/\\]*"
MATCH_RECURSIVE = r"(?:.*)"


def glob_to_re(pattern: str) -> str:
    """Translate a glob pattern to a regular expression for matching."""
    raise NotImplementedError


def match_glob(path: Path, pattern: str) -> bool:
    """Check if a path matches a glob pattern.

    If the pattern ends with a directory separator, the path must be a directory.
    """
    raise NotImplementedError
