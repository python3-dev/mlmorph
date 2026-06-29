#!/usr/bin/env python

from importlib import resources
from typing import Any

import regex
import sfst  # ty: ignore[unresolved-import]

from .foreign_word_detector import check_foreign_word
from .normalizer import normalize


class Analyser:
    ANALYSER_REGEX = regex.compile(r"((?P<root>([^<])+)(?P<tags>(<[^>]+>)+))+")
    POS_REGEX = regex.compile(r"(<(?P<tag>([^>]+))>)+")
    RESOURCE_PATH = "data/malayalam.a"

    def __init__(self) -> None:
        """Construct Mlmorph Analyser."""
        self.fsa: str | None = None
        if resources.files("mlmorph").joinpath(Analyser.RESOURCE_PATH).is_file():
            self.fsa = str(resources.files("mlmorph").joinpath(Analyser.RESOURCE_PATH))
        if not self.fsa:
            raise ValueError("Could not read the fsa.")
        sfst.init(self.fsa)

    def analyse(
        self, word: str, weighted: bool = True, foreign_word_check: bool = True
    ) -> list[str] | list[tuple[str, int]]:
        """
        Perform a morphological analysis lookup.

        Parameters
        ----------
        word : str
            The word to analyse.
        weighted : bool, optional
            Return results with analyser weights. Default is True.
        foreign_word_check : bool, optional
            Apply the foreign-word detector to words with no analysis. Default is True.

        Returns
        -------
        list[str] | list[tuple[str, int]]
            When weighted is False, a list of raw analysis strings.
            When weighted is True, a list of (analysis, weight) tuples sorted
            by ascending weight (best analysis first).
        """
        word = normalize(word)
        analysis_results = sfst.analyse(word)
        if not len(analysis_results):
            if foreign_word_check and check_foreign_word(word):
                analysis_results = [word + "<fw>"]

        if not weighted:
            return analysis_results

        processed_result = []
        for analysis in analysis_results:
            parsed_result = Analyser.parse_analysis(analysis)
            processed_result.append((analysis, parsed_result["weight"]))

        return sorted(processed_result, key=lambda tup: tup[1])

    @staticmethod
    def parse_analysis(analysis: str) -> dict[str, Any]:
        """
        Parse an analysis string into a structured dict.

        Parameters
        ----------
        analysis : str
            Raw SFST analysis string of the form ``root<tag1><tag2>...``.

        Returns
        -------
        dict[str, Any]
            Dictionary with keys:

            - ``morphemes``: list of dicts, each with ``root`` (str) and
              ``pos`` (list[str]).
            - ``weight``: int, lower is better.

        Raises
        ------
        ValueError
            If the analysis string cannot be parsed.
        """
        result: dict[str, Any] = {}
        if analysis is None:
            return result

        if analysis[0] == "<":
            analysis = " " + analysis
        match = Analyser.ANALYSER_REGEX.match(analysis)
        if not match:
            raise ValueError("Could not parse the analysis." + analysis)
        roots = match.captures("root")
        morphemes = []
        for rindex in range(len(roots)):
            morpheme: dict[str, Any] = {}
            morpheme["root"] = roots[rindex]
            tags = match.captures("tags")[rindex]
            morpheme["pos"] = Analyser.POS_REGEX.match(tags).captures("tag")
            morphemes.append(morpheme)

        result["morphemes"] = morphemes
        result["weight"] = Analyser.get_weight(morphemes)
        return result

    @staticmethod
    def get_weight(analysis: list[dict[str, Any]]) -> int:
        """
        Compute a preference weight for an analysis; lower is better.

        Parameters
        ----------
        analysis : list[dict[str, Any]]
            List of morpheme dicts as returned by ``parse_analysis``.

        Returns
        -------
        int
            Composite weight based on morpheme count, POS tags, and root length.
        """
        morpheme_length = len(analysis)
        weight = morpheme_length * 100
        for i in range(morpheme_length):
            pos = analysis[i]["pos"]
            root = analysis[i]["root"]
            for j in range(len(pos)):
                weight += len(pos) * 5 + len(root) * 2 + Analyser.get_pos_weight(pos[j]) * 3
        return weight

    @staticmethod
    def get_pos_weight(pos: str) -> int:
        """
        Return the relative preference weight for a POS tag.

        Parameters
        ----------
        pos : str
            POS tag string (e.g. ``"v"``, ``"n"``, ``"np"``).

        Returns
        -------
        int
            Lower weight indicates a preferred POS tag. Falls back to tag length.
        """
        WEIGHTS = {
            "v": 1,
            "n": 2,
            "adv": 3,
            "adj": 4,
            "coordinative": 4,
            "v-n-compound": 4,
            "prn": 5,
            "past": 4,
            "cvb-adv-part-past": 5,
            "np": 5,
            "fw": 1,
        }
        return WEIGHTS.get(pos, len(pos))
