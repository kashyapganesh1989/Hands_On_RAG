"""Gate 2 — PII & Secrets redaction. Scrubs chunks BEFORE the context window
and answers BEFORE display. The model cannot leak what it never saw.

NOTE: regex patterns are the teaching baseline. Production stacks layer
NER-based detection (e.g. Microsoft Presidio) on top of this."""

import re


class PIIRedactor:
    def __init__(self, patterns: dict[str, str]):
        self._patterns = {label: re.compile(p, re.IGNORECASE) for label, p in patterns.items()}

    def redact(self, text: str) -> tuple[str, list[dict]]:
        """Returns (redacted_text, findings). Findings record WHAT was caught
        for the audit trail — never the secret itself."""
        findings = []
        redacted = text
        for label, rx in self._patterns.items():
            matches = rx.findall(redacted)
            if matches:
                findings.append({"type": label, "count": len(matches)})
                redacted = rx.sub(f"[REDACTED-{label}]", redacted)
        return redacted, findings
