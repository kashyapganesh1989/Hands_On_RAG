"""Gate 1 — Content Filter. Catches prompt injection in user input AND
retrieved chunks, BEFORE the model is called. A blocked attack costs zero tokens."""

import re


class ContentFilter:
    def __init__(self, patterns: list[str]):
        self._patterns = [re.compile(p, re.IGNORECASE) for p in patterns]

    def check(self, text: str) -> tuple[bool, str]:
        """Returns (is_safe, reason)."""
        for rx in self._patterns:
            if rx.search(text):
                return False, (
                    f"Blocked by Gate 1 (Content Filter): matched injection pattern "
                    f"'{rx.pattern}'"
                )
        return True, "clean"
