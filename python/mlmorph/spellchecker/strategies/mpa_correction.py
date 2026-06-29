from collections.abc import Iterator

from .suggestion_strategy import SuggestionStrategy


class MpaCorrection(SuggestionStrategy):
    """
    Replace ന്പ, ൻപ, ംപ, ംമ്പ with മ്പ
    """

    def suggest(self, word: str) -> Iterator[str]:
        candidate = word.replace("ന്പ", "മ്പ")
        if candidate != word:
            yield candidate
        candidate = word.replace("ൻപ", "മ്പ")
        if candidate != word:
            yield candidate
        candidate = word.replace("ംപ", "മ്പ")
        if candidate != word:
            yield candidate
        candidate = word.replace("ംമ്പ", "മ്പ")
        if candidate != word:
            yield candidate
