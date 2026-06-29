"""
TDD tests for type correctness and code quality improvements.

These tests enforce the audit requirements before implementation,
following red-green-refactor discipline.
"""

import ast
import inspect
import textwrap


def _source_uses_module(func_or_class, module_name: str) -> bool:
    """Return True if the source of func_or_class contains an import of module_name."""
    source = inspect.getsourcefile(func_or_class)
    if source is None:
        return False
    with open(source) as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == module_name:
                    return True
        if isinstance(node, ast.ImportFrom):
            if node.module == module_name:
                return True
    return False


def test_spellchecker_all_entries_are_strings():
    """spellchecker.__all__ must contain strings, not class objects."""
    import mlmorph.spellchecker.spellchecker as sc

    for entry in sc.__all__:
        assert isinstance(entry, str), f"__all__ entry {entry!r} is not a string"


def test_foreign_word_detector_uses_regex_not_re():
    """foreign_word_detector must use the `regex` package, not stdlib `re`."""
    import mlmorph.foreign_word_detector as fwd

    assert not _source_uses_module(fwd.check_foreign_word, "re"), (
        "foreign_word_detector.py uses `import re`; should use `import regex`"
    )


def test_suggestion_strategy_uses_regex_not_re():
    """SuggestionStrategy must use the `regex` package, not stdlib `re`."""
    from mlmorph.spellchecker.strategies.suggestion_strategy import SuggestionStrategy

    assert not _source_uses_module(SuggestionStrategy, "re"), (
        "suggestion_strategy.py uses `import re`; should use `import regex`"
    )


def test_has_sure_patterns_returns_bool():
    """has_sure_patterns must return a bool, not a Match object."""
    from mlmorph.foreign_word_detector import has_sure_patterns

    result = has_sure_patterns("hello")
    assert isinstance(result, bool), (
        f"has_sure_patterns must return bool, got {type(result).__name__}"
    )


def test_spellchecker_does_not_use_importlib_for_strategies():
    """candidates_from_strategies must not use importlib.import_module."""
    from mlmorph.spellchecker.spellchecker import SpellChecker

    source = inspect.getsource(SpellChecker.candidates_from_strategies)
    tree = ast.parse(textwrap.dedent(source))
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr == "import_module":
            raise AssertionError(
                "candidates_from_strategies still uses importlib.import_module; "
                "use direct class references instead"
            )
