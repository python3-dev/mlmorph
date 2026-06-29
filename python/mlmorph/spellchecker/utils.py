import csv
import pkgutil


def read_common_mistakes() -> dict[str, str]:
    """
    Load the common-mistakes database bundled with the package.

    Returns
    -------
    dict[str, str]
        Mapping of misspelled word to its correct form.

    Raises
    ------
    RuntimeError
        If the bundled CSV resource cannot be read.
    """
    data = pkgutil.get_data(__name__, "resources/common_mistakes.csv")
    if data is None:
        raise RuntimeError("Could not load common_mistakes.csv resource")
    reader = csv.DictReader(data.decode("utf-8").splitlines(), delimiter=",")
    return {row["word"]: row["correct"] for row in reader}
