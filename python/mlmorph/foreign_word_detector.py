#!/usr/bin/env python

import regex

ENGLISH_PATTERNS = [
    "\\S+[അ-ഔ]\\S+",
    "\\S+റ്റ്\\S+",
    "^ജെ",
    "^ട",
    "^ഡ",
    "^ഫാ",
    "^ഫി",
    "^ഫീ",
    "^ഫു",
    "^ഫെ",
    "^ഫെ",
    "^ഫൈ",
    "^ഫൊ",
    "^ഫോ",
    "^ബാൻ",
    "^ബാറ്റ്",
    "^ബെ",
    "^മെറ്റ",
    "മ്യൂ",
    "^ഷോ",
    "^സ്ക്രീ",
    "^ഹാ",
    "^ഹി",
    "^ഹെ",
    "^ഹൊ",
    "^ഹോ",
    "^ഹൗ",
    "^ഹ്യ",
    "^ഹ്വ",
    "^ള",
    "^ഴ",
    "^റ",
    "^റോ",
    "^റ്റൈ",
    "ഓൺ",
    "ക്ച",
    "ക്ട്$",
    "ക്യൂ",
    "ക്സ",
    "ക്ലോ",
    "ക്റ്റ്",
    "ഗ്രഫ",
    "ഗ്രഫി",
    "ഗിൾ",
    "ങ്സ്",
    "ച്വ",
    "ജ്യു",
    "ജ്യൂ",
    "ട്ര",
    "ഡിയോ",
    "ഡ്$",
    "ഡ്ക",
    "ഡ്മ",
    "ഡ്വ",
    "ഡ്സ",
    "ണിയൻ$",
    "ണിയർ$",
    "ണ്ടർ$",
    "ൻഡ",
    "ൻസ്",
    "ന്റം",
    "ന്റിക്",
    "ന്റ്$",
    "ന്റ്സ്",
    "ൻ്റ്$",
    "ന്റർ",
    "പ്രൊ",
    "പ്സ്$",
    "പ്റ്റ",
    "ഫ്ര",
    "ഫ്ല",
    "ഫ്ള",
    "ഫ്റ്റ",
    "ഫൈ",
    "ബിൻ",
    "ബിർ",
    "ബിൽ",
    "ബിൾ",
    "ബിറ്റ്",
    "ബെർ",
    "ബൈ",
    "ബ്രേ",
    "ബ്രോ",
    "ബ്ല",
    "ബ്സ",
    "ബ്ള",
    "മെമ്മ",
    "മൈസ",
    "മ്പ്യൂ",
    "യിറ്റ്",
    "യ്ൻ",
    "യ്സ",
    "യ്സ്",
    "യിസ",
    "യ്റ്റ്",
    "ർജ",
    "ർട",
    "ലിറ്റി",
    "ലീസ്",
    "ലൈസർ",
    "ൽസ്",
    "വെയർ$",
    "വൈസ്",
    "വേസ്",
    "ഷിസ്",
    "ഷ്യൻ$",
    "ഷ്യർ$",
    "ഷ്യൽ$",
    "ഷ്യസ്$",
    "സബ്",
    "സർ$",
    "സൽ$",
    "സെൽ",
    "സെർ",
    "സെൻ",
    "സിസ്",
    "സിറ്റി",
    "സെന്റ",
    "സ്കൂൾ",
    "സ്പേസ്",
    "സൈറ്റ",
    "സ്പ്ല",
    "സ്പ്ള",
    "സ്ബ",
    "സ്ല",
    "സ്ള",
    "സ്കാൻ",
    "സ്കോ",
    "സ്റ്റ",
    "^സ്വീ",
    "സ്ല",
    "സ്ട്ര",
    "ളജി",
    "ൾട്ട",
    "ഴ്സ",
    "റ്റിക്$",
    "റ്റിക്കലി$",
    "റ്റേൺ",
    "റ്ററ",
    "റ്റർ",
    "റ്റലൈ",
    "റൈറ്റ",
    "ിംഗ്$",
    "ിങ്$",
    "ിങ്ങ്$",
    "ിഷൻ",
    "ിസം$",
    "ിംസ്",
    "ീസ്$",
    "േഷൻ",
    "ൈറ്റ",
    "ോഷൻ",
    "ൗണ്ട",
    "്രീം",
    "ക്വേ",
    "[0-9]+",
]

compiled_english_pattern_regex = regex.compile("|".join(ENGLISH_PATTERNS))


def check_foreign_word(word: str) -> int:
    """
    Detect whether a word is foreign (non-native Malayalam).

    Parameters
    ----------
    word : str
        The word to check.

    Returns
    -------
    int
        1 if the word is foreign, 0 if it appears to be native Malayalam.
    """
    word = word.strip()
    # Remove all ZWS, ZWNJ, ZWJ before pattern matching
    word = regex.sub(r"[​-‍]", "", word)
    if not is_valid_malayalam_word(word):
        # Unknown word. Surely foreign
        return 1
    if has_sure_patterns(word):
        return 1
    return 0


def has_sure_patterns(word: str) -> bool:
    """
    Check whether the word matches any known foreign-word pattern.

    Parameters
    ----------
    word : str
        The word to check.

    Returns
    -------
    bool
        True if a foreign pattern is found, False otherwise.
    """
    return regex.search(compiled_english_pattern_regex, word) is not None


def is_valid_malayalam_word(word: str) -> bool:
    """
    Return True if the word contains valid Malayalam Unicode characters.

    Parameters
    ----------
    word : str
        The word to validate.

    Returns
    -------
    bool
        True if the word is a valid Malayalam word candidate, False otherwise.
    """
    if len(word) <= 1:
        return False
    # Ignore all non-Malayalam words
    if regex.search(r"[ഀ-ൿ‌-‍]+", word) is None:
        return False
    return True
