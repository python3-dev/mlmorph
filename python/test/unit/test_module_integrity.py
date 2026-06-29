"""Tests for module-level invariants that don't require a compiled FSA."""

import ast
import inspect
import textwrap

from mlmorph.generator import Generator


def test_generator_init_uses_own_resource_path():
    """Bug #1: Generator.__init__ must reference Generator.RESOURCE_PATH, not Analyser's."""
    source = inspect.getsource(Generator.__init__)
    tree = ast.parse(textwrap.dedent(source))
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Attribute)
            and node.attr == "RESOURCE_PATH"
            and isinstance(node.value, ast.Name)
            and node.value.id == "Analyser"
        ):
            raise AssertionError(
                "Generator.__init__ references Analyser.RESOURCE_PATH; "
                "it should reference Generator.RESOURCE_PATH"
            )


def test_generator_resource_path_attribute_exists():
    """Generator must declare its own RESOURCE_PATH, not rely on Analyser's."""
    assert hasattr(Generator, "RESOURCE_PATH"), "Generator is missing RESOURCE_PATH"
    assert isinstance(Generator.RESOURCE_PATH, str)
