from collections.abc import Iterator

from .suggestion_strategy import SuggestionStrategy


class NtaCorrection(SuggestionStrategy):
    """
    Replace ൻറ, ൻ്റ with ന്റ
    """

    def suggest(self, word: str) -> Iterator[str]:
        candidate = word.replace("ൻറ", "ന്റ")
        if candidate != word:
            yield candidate
        candidate = word.replace("ൻ്റ", "ന്റ")
        if candidate != word:
            yield candidate
