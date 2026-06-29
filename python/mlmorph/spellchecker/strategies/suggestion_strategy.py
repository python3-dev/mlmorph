import abc
from collections.abc import Iterator
from itertools import product

import regex


class SuggestionStrategy(metaclass=abc.ABCMeta):
    """
    Abstract base for all spelling-suggestion strategies.

    Each concrete subclass implements one algorithm for generating candidate
    corrections for a misspelled word.
    """

    @abc.abstractmethod
    def suggest(self, word: str) -> Iterator[str]:
        """
        Yield candidate corrections for *word*.

        Parameters
        ----------
        word : str
            The misspelled word to correct.

        Yields
        ------
        str
            Candidate corrections, in strategy-defined order.
        """

    def isConsonant(self, char: str) -> bool:
        """
        Return True if *char* is a Malayalam consonant (ക–ഹ range).

        Parameters
        ----------
        char : str
            A single Unicode character.

        Returns
        -------
        bool
            True if the character is a Malayalam consonant.
        """
        return regex.compile(r"([ക-ഹ])").search(char) is not None

    def getCandidatesWithReplacements(self, word: str, letters: str) -> Iterator[str]:
        """
        Yield variants of *word* where each letter in *letters* is swapped.

        Parameters
        ----------
        word : str
            The source word.
        letters : str
            Set of characters; each position in *word* whose current character
            belongs to *letters* is replaced in turn with each other character
            in *letters*.

        Yields
        ------
        str
            Modified word variants.
        """
        orig_letter_list = list(word)
        for replacement, pos in product(letters, range(len(word))):
            original = orig_letter_list[pos]
            if original in letters:
                orig_letter_list[pos] = replacement
                yield "".join(orig_letter_list)
