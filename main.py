#!/usr/bin/env python3
"""One-word entry for the make.fun boss bounty.

The task: exactly one word (30 characters or fewer) describing your boss.
This entry is "Hovercraft" -- the boss who never lands, just hovers
over your shoulder, humming, watching every keystroke, never quite
touching down or going away.

The script validates the word, prints exactly that word to stdout,
and writes it to the output file for the bounty harness.
"""

import os
import sys

ENTRY = "Hovercraft"


def validate(word):
    """Check the entry is exactly one word, 1-30 characters, no spaces."""
    if not word:
        raise ValueError("entry must not be empty")
    if len(word) > 30:
        raise ValueError("entry must be 30 characters or fewer")
    if len(word.split()) != 1:
        raise ValueError("entry must be exactly one word")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must contain no whitespace")
    if not word.isalpha():
        raise ValueError("entry must be letters only, no punctuation")
    if word != word.strip():
        raise ValueError("entry must not have leading or trailing space")
    return word


def revalidate_printed(word):
    """Re-check the exact bytes about to be printed, as a final guard."""
    rendered = word + "\n"
    if rendered.strip() != word or len(rendered.strip().split()) != 1:
        raise ValueError("printed output would not be exactly one word")
    return rendered


def output_path():
    """Resolve where to write the entry file.

    Prefer $MAKEFUN_OUTPUT when set, then /output/entry.txt, and fall
    back to ./output/entry.txt when /output is not writable.
    """
    env_dir = os.environ.get("MAKEFUN_OUTPUT")
    if env_dir:
        return os.path.join(env_dir, "entry.txt")
    return "/output/entry.txt"


def write_entry(word, path):
    """Write the word to path, then read it back to verify the write."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(word + "\n")
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read().strip()
    if written != word:
        raise ValueError("read-back verification failed: file mismatch")
    return path


def main():
    word = validate(ENTRY)
    rendered = revalidate_printed(word)
    sys.stdout.write(rendered)
    sys.stdout.flush()
    try:
        write_entry(word, output_path())
    except (OSError, ValueError) as exc:
        # Fall back to a local output directory; the printed word is
        # still the entry, so a failed write only warns on stderr.
        try:
            write_entry(word, os.path.join("output", "entry.txt"))
        except (OSError, ValueError):
            print(f"warning: could not write entry file: {exc}",
                  file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
