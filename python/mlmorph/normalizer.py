normalization_map = {
    "ണ്‍": "ൺ",
    "ന്‍": "ൻ",
    "ര്‍": "ർ",
    "ല്‍": "ൽ",
    "ള്‍": "ൾ",
    "ക്‍": "ൿ",
    "ൻ്റ": "ന്റ",
    "ൌ": "ൗ",
}


def normalize(text: str) -> str:
    """
    Normalise Malayalam text by replacing archaic glyph sequences with atomic forms.

    Parameters
    ----------
    text : str
        Input text to normalise.

    Returns
    -------
    str
        Text with legacy chillu/vowel sequences replaced by their atomic Unicode forms.
    """
    for key in normalization_map:
        text = text.replace(key, normalization_map[key])
    return text
