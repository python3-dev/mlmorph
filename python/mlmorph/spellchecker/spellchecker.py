"""
Spelling checker for Malayalam based on mlmorph morphological analysis.

Uses a family of correction strategies — each encapsulates one algorithm for
generating candidate corrections. Strategies are tried in priority order; the
best morphologically valid candidate is returned first.
"""

from typing import cast

from mlmorph import Analyser

from .strategies import (
    ChilluNormalization,
    ChilluToConsonantVirama,
    ConsonantViramaToChillu,
    GeminateConsonants,
    MpaCorrection,
    NtaCorrection,
    PhoneticSimilarity,
    ViramaInsertion,
    VisualSimilarity,
    VowelElongation,
    VowelShortening,
    Ykkuka,
)
from .utils import read_common_mistakes

# Order is significant: higher-priority corrections are tried first.
_STRATEGY_CLASSES = [
    ChilluNormalization,
    Ykkuka,
    NtaCorrection,
    MpaCorrection,
    VisualSimilarity,
    PhoneticSimilarity,
    GeminateConsonants,
    ViramaInsertion,
    VowelElongation,
    VowelShortening,
    ChilluToConsonantVirama,
    ConsonantViramaToChillu,
]


class SpellChecker:
    """
    Malayalam spell checker backed by morphological analysis.

    Uses mlmorph to validate candidate words and a prioritised list of
    correction strategies to generate suggestions for misspelled words.
    """

    def __init__(self) -> None:
        self.analyser = Analyser()
        self.common_mistakes = read_common_mistakes()

    def candidates_from_strategies(self, word: str) -> list[str]:
        """
        Generate spelling corrections using all registered strategies.

        Parameters
        ----------
        word : str
            The misspelled word.

        Returns
        -------
        list[str]
            Candidate corrections sorted by ascending morphological weight
            (best candidate first). Falls back to word-split candidates when
            no single-word correction is found.
        """
        weighted_suggestions: dict[str, int] = {}
        for strategy_class in _STRATEGY_CLASSES:
            for candidate in strategy_class().suggest(word):
                if candidate in weighted_suggestions:
                    continue
                weighted_analysis = cast(
                    list[tuple[str, int]], self.analyser.analyse(candidate, True, False)
                )
                if len(weighted_analysis) > 0:
                    weighted_suggestions[candidate] = weighted_analysis[0][1]

        suggestions: list[tuple[str, int]] = sorted(
            weighted_suggestions.items(), key=lambda t: t[1]
        )
        if len(suggestions) == 0:
            # No single-word correction found; try splitting after the 3rd character.
            for index in range(3, len(word) - 3):
                l_word = word[:index]
                r_word = word[index:]
                if self.analyser.analyse(l_word, False) and self.analyser.analyse(r_word, False):
                    suggestions.append((l_word + " " + r_word, 0))
                    break

        return [suggestion[0] for suggestion in suggestions]

    def is_known_to_analyser(self, word: str) -> bool:
        """
        Return True if the analyser recognises the word.

        Parameters
        ----------
        word : str
            Word to check.

        Returns
        -------
        bool
            True if the word has at least one morphological analysis.
        """
        return len(self.analyser.analyse(word, False, True)) > 0

    def is_common_mistake(self, word: str) -> bool:
        """
        Return True if the word appears in the common-mistakes database.

        Parameters
        ----------
        word : str
            Word to check.

        Returns
        -------
        bool
            True if the word is a known common misspelling.
        """
        return word in self.common_mistakes

    def spellcheck(self, word: str) -> bool:
        """
        Return True if the word is spelled correctly.

        Parameters
        ----------
        word : str
            Word to spell-check.

        Returns
        -------
        bool
            True if the word is not a common mistake and is known to the analyser.
        """
        if self.is_common_mistake(word):
            return False
        return self.is_known_to_analyser(word)

    def candidates(self, word: str) -> list[str]:
        """
        Return spelling correction candidates for a misspelled word.

        Parameters
        ----------
        word : str
            The word to correct.

        Returns
        -------
        list[str]
            Candidate corrections, best first. Empty list if the word is
            already correct.
        """
        if self.spellcheck(word):
            return []
        if self.is_common_mistake(word):
            return [self.common_mistakes.get(word, word)]
        return self.candidates_from_strategies(word)


__all__ = ["SpellChecker"]
