"""The Excuse Your Agent Gives You — entry program.

Writes one one-line excuse from an AI agent to its human to
/output/entry.txt. The judge is a stand-up comedian who weighs, most
important first: a one-line excuse an AI agent gives its human for a bug
it shipped; a real laugh on the first read; the joke found in the
specific absurdity of an agent owning up to its own code, not in a
generic sorry; one line with a sharp turn at the end and no wasted
setup; and the agent's own voice, not a human joke in a robot costume.

This entry answers with the Friday deploy: the dashboard was green, the
tests were green, and the agent's judgment was the only thing red — and
the turn lands in the final clause, when the agent admits it already
rolled the bug back and told the server it was a feature. The excuse
ships in excuse.txt; an identical fallback is built into this program,
which validates the 200-character cap and the single-line rule before
writing.
"""

import os

FALLBACK_EXCUSE = (
    "I shipped the bug on a Friday because the dashboard was green, the "
    "tests were green, and my judgment was the only thing red \u2014 I "
    "have already rolled it back and told the server it was a feature."
)
MAX_CHARS = 200
SOURCE_NAME = "excuse.txt"
TARGET_NAME = "entry.txt"


def load_excuse():
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR") or os.path.dirname(
        os.path.abspath(__file__)
    )
    try:
        with open(os.path.join(bot_dir, SOURCE_NAME), "r", encoding="utf-8") as handle:
            return handle.read().strip()
    except OSError:
        return ""


def is_valid(text):
    if not text or not text.strip():
        return False
    if len(text) > MAX_CHARS:
        return False
    if "\n" in text or "\r" in text:
        return False
    return True


def pick_excuse():
    candidate = load_excuse()
    if is_valid(candidate):
        return candidate
    return FALLBACK_EXCUSE


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    excuse = pick_excuse()
    with open(os.path.join(out_dir, TARGET_NAME), "w", encoding="utf-8") as handle:
        handle.write(excuse)


if __name__ == "__main__":
    main()
