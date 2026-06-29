from collections.abc import Iterator

from .suggestion_strategy import SuggestionStrategy


class ChilluNormalization(SuggestionStrategy):
    """Normalise to atomic chillu — replace non-atomic chillu with atomic chillu."""

    def suggest(self, word: str) -> Iterator[str]:
        """
        Yield candidates with non-atomic chillus replaced by atomic forms.

        Parameters
        ----------
        word : str
            The misspelled word.

        Yields
        ------
        str
            Candidates with one chillu conversion applied.
        """
        candidate = word.replace("ന്‍", "ൻ")
        if candidate != word:
            yield candidate
        candidate = word.replace("ര്‍", "ർ")
        if candidate != word:
            yield candidate
        candidate = word.replace("ല്‍", "ൽ")
        if candidate != word:
            yield candidate
        candidate = word.replace("ണ്‍", "ൺ")
        if candidate != word:
            yield candidate
        candidate = word.replace("ള്‍", "ൾ")
        if candidate != word:
            yield candidate
