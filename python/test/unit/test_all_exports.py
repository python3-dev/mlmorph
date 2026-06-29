"""Tests for the public API surface exposed via __all__."""

import mlmorph


def test_all_entries_are_strings():
    """Bug #2: __all__ must contain only strings, not function objects.

    Bare function references in __all__ cause `from mlmorph import *` to raise
    TypeError at import time. Every entry must be the quoted name of the symbol.
    """
    for entry in mlmorph.__all__:
        assert isinstance(entry, str), (
            f"__all__ entry {entry!r} is not a string — "
            f"use the quoted name '{entry.__name__}' instead"
        )


def test_all_exports_are_importable():
    """Every name in __all__ must be resolvable as an attribute of the module."""
    for name in mlmorph.__all__:
        assert hasattr(mlmorph, name), (
            f"'{name}' is listed in __all__ but not importable from mlmorph"
        )
