from collections.abc import Iterator

from .suggestion_strategy import SuggestionStrategy


class VowelShortening(SuggestionStrategy):
    """
    Implement the algorithm using the Strategy interface.
    """

    shortening_map = {"ാ": "", "ീ": "ി", "ൂ": "ു", "േ": "െ", "ോ": "ൊ"}

    def suggest(self, word: str) -> Iterator[str]:
        start = 1
        for i in range(start, len(word)):
            candidate = list(word)
            char = candidate[i]
            if char in self.shortening_map:
                candidate[i] = self.shortening_map[char]
                start = i + 1
                yield "".join(candidate)
                continue
