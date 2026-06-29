import regex


def tokenize(text: str) -> list[str]:
    """
    Split text into word tokens, stripping punctuation and whitespace.

    Parameters
    ----------
    text : str
        Input text to tokenise.

    Returns
    -------
    list[str]
        List of word tokens with leading/trailing punctuation removed.
    """
    words = regex.split(r"[-+#\.\s?!\(\)\[\]:,;]", text)
    strip_pattern = r"^[ '?|/!@#$%^&*()_+=`{}\[\]‌]+|[ '?|/!@#$%^&*()_+=`{}\[\]‌]+$"
    return [regex.sub(strip_pattern, "", word) for word in words]
