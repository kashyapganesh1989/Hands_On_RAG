"""Gate 3 — Policy Check. The agent's job description, enforced in code.
This assistant is READ-ONLY: it answers questions; it does not mutate,
send, or spend. A junior employee has no signing authority — neither does this agent."""

import re


class PolicyCheck:
    def __init__(self, forbidden_patterns: list[str]):
        self._patterns = [re.compile(p, re.IGNORECASE) for p in forbidden_patterns]

    def check(self, text: str) -> tuple[bool, str]:
        """Returns (is_allowed, reason)."""
        for rx in self._patterns:
            if rx.search(text):
                return False, (
                    "Blocked by Gate 3 (Policy Check): this assistant is read-only. "
                    f"Requested action matches forbidden pattern '{rx.pattern}'"
                )
        return True, "within policy"
