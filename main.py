#!/usr/bin/env python3
"""Word-delete entry: emit exactly one dictionary word, nothing else.

The word names the fear of long words, in its popular 36-letter form.
Erasing it from the dictionary also erases the phobia's own name, and
the name itself is one of the longest words in the dictionary, so the
joke is carried by the word alone, with no setup attached.
"""

from __future__ import annotations

import os
import sys

WORD = "hippopotomonstrosesquippedaliophobia"
EXPECTED_LEN = 36
FALLBACK_DIR = "/output"
FILENAME = "entry.txt"
ENV_VAR = "MAKEFUN_OUTPUT_DIR"


class EntryProblem(Exception):
    """Raised when the entry word or its destination is not usable."""


def destination_dir() -> str:
    """Return the folder the grader collects outputs from."""
    wanted = os.environ.get(ENV_VAR)
    if wanted:
        return wanted
    return FALLBACK_DIR


def payload(word: str) -> bytes:
    """Check the word is exactly one bare word, then encode it."""
    if not word:
        raise EntryProblem("entry word is empty")
    if word != word.strip():
        raise EntryProblem("entry word has surrounding whitespace")
    if any(ch.isspace() for ch in word):
        raise EntryProblem("entry must be a single word with no spaces")
    if len(word) != EXPECTED_LEN:
        raise EntryProblem(
            "entry word is %d letters, expected %d" % (len(word), EXPECTED_LEN)
        )
    return word.encode("utf-8")


def write_entry(data: bytes) -> str:
    """Write the word to entry.txt and confirm the read-back matches."""
    folder = destination_dir()
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, FILENAME)
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, 0o644)
    with open(path, "rb") as handle:
        back = handle.read()
    if back != data:
        raise EntryProblem("entry.txt read-back does not match the word")
    return path


def main(argv: list[str]) -> int:
    """Validate the word, write it out, report where it landed."""
    if len(argv) > 1:
        raise EntryProblem("this entry takes no arguments")
    data = payload(WORD)
    path = write_entry(data)
    sys.stdout.write("wrote %d letters to %s\n" % (len(data), path))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except EntryProblem as problem:
        sys.stderr.write("error: %s\n" % problem)
        sys.exit(1)
