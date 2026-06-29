import csv
import glob
import mmap
import os

import regex
from mlmorph import Analyser, tokenize
from rich.progress import track


def is_valid_malayalam_word(word: str) -> bool:
    word = word.strip()
    if len(word) <= 1:
        return False
    if regex.search(r"[ഀ-ൿ‌-‍]+", word) is None:
        return False
    return True


def get_words(file_path: str) -> list[str]:
    words = []
    with open(file_path, "r") as f:
        map_file = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
        for line in iter(map_file.readline, b""):
            tokens = tokenize(line.decode("utf-8"))
            for word in tokens:
                if is_valid_malayalam_word(word):
                    words.append(word)
    return words


analyser = Analyser()

csvfilename = "mlmorph.csv"
with open(csvfilename, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["word", "analysis"])
    files = glob.glob(os.path.join("tests", "coverage", "*.txt"))
    for filename in files:
        words = get_words(filename)
        rows = []
        for word in track(words, description=filename):
            analysis = analyser.analyse(word, True)
            if len(analysis) > 0:
                rows.append([word, analysis[0][0]])
        csvwriter.writerows(rows)
