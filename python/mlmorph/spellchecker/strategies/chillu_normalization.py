from .suggestion_strategy import SuggestionStrategy


class ChilluNormalization(SuggestionStrategy):
    """
    Normalize to atomic chillu - Replace any non-atomic chillu to atomic chillu
    """

    def suggest(self, word):
        candidates = []
        candidate = word.replace("ന്\u200d", "ൻ")
        if candidate != word:
            yield candidate
        candidate = word.replace("ര്\u200d", "ർ")
        if candidate != word:
            yield candidate
        candidate = word.replace("ല്\u200d", "ൽ")
        if candidate != word:
            yield candidate
        candidate = word.replace("ണ്\u200d", "ൺ")
        if candidate != word:
            yield candidate
        candidate = word.replace("ള്\u200d", "ൾ")
        if candidate != word:
            yield candidate
        return candidates
