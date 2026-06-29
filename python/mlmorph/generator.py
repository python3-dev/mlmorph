#!/usr/bin/env python

from importlib import resources

import sfst  # ty: ignore[unresolved-import]

from .analyser import Analyser
from .normalizer import normalize


class Generator:
    RESOURCE_PATH = "data/malayalam.a"

    def __init__(self) -> None:
        """Construct Mlmorph Generator."""
        self.fsa: str | None = None
        if resources.files("mlmorph").joinpath(Generator.RESOURCE_PATH).is_file():
            self.fsa = str(resources.files("mlmorph").joinpath(Generator.RESOURCE_PATH))
        if not self.fsa:
            raise ValueError("Could not read the fsa.")
        sfst.init(self.fsa)

    @staticmethod
    def get_weight(generated_word: str, token: str) -> int:
        """
        Compute a preference weight for a generated word form.

        Prefers shorter words and common inflectional suffixes.

        Parameters
        ----------
        generated_word : str
            The generated surface form to score.
        token : str
            The generator input token (used to derive a base weight).

        Returns
        -------
        int
            Composite weight; lower is more preferred.
        """
        suffixes = ["ിൽ", "ിലും", "ന്റെ", "ന്", "നെ"]
        token_weight = Analyser.parse_analysis(token)["weight"]
        weight = token_weight
        for i, suffix in enumerate(suffixes):
            if generated_word.endswith(suffix):
                return weight + i
        return weight + len(generated_word)

    def generate(self, token: str, weighted: bool = True) -> list[tuple[str, int]] | tuple:
        """
        Perform a morphological generation lookup.

        Parameters
        ----------
        token : str
            The morphological representation to generate surface forms for
            (e.g. ``"മലയാളം<n><pl>"``).
        weighted : bool, optional
            When True, return results sorted by weight. Default is True.

        Returns
        -------
        list[tuple[str, int]] | tuple
            When weighted is True, a list of (surface_form, weight) tuples
            sorted by ascending weight (best form first).
            When weighted is False, the raw list returned by the FST.
        """
        token = normalize(token)
        generated_results = sfst.generate(token)
        if not weighted:
            return generated_results

        processed_result = []
        for generated_word in generated_results:
            processed_result.append((generated_word, Generator.get_weight(generated_word, token)))
        return sorted(processed_result, key=lambda tup: tup[1])
