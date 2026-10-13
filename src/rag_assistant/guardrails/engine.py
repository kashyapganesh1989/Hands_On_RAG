"""The Five Gates safety engine.

Gate 1 — Content Filter   guard_input()   blocks prompt-injection attempts
Gate 2 — PII Redactor     guard_chunks()/guard_output()   strips private data
Gate 3 — Policy Check     guard_input()   blocks any non-read-only request
Gate 4 — Rate Limiter     .limiter        caps calls & estimated tokens
Gate 5 — Audit Trail      via AuditLogger  tamper-evident hash-chained log

Rules live in guardrails.yaml, not in code, so they can be tuned without a
release. Only decisions worth remembering are written to the audit log: a
block, or a redaction — an ordinary allowed question with nothing to redact
leaves no trace, by design (there's nothing to prove).
"""

import re
from pathlib import Path

import yaml

from rag_assistant.guardrails.rate_limiter import RateLimiter

# Checked, and reported, in this fixed order.
_PII_ORDER = ["SSN", "EMAIL", "PHONE", "API-KEY", "AWS-KEY"]


class GuardrailEngine:
    def __init__(self, config_path, audit_logger):
        self.config_path = Path(config_path)
        self.audit = audit_logger
        self.events = []

        config = yaml.safe_load(self.config_path.read_text(encoding="utf-8")) or {}

        self.content_filter_patterns = list(config.get("content_filter", {}).get("patterns", []))
        self.policy_patterns = list(config.get("policy", {}).get("forbidden_patterns", []))

        pii_config = {rule["label"]: rule["pattern"] for rule in config.get("pii", {}).get("patterns", [])}
        self.pii_rules = [(label, pii_config[label]) for label in _PII_ORDER if label in pii_config]

        rate_config = config.get("rate_limit", {})
        self.limiter = RateLimiter(
            max_calls_per_session=rate_config.get("max_calls_per_session", 10),
            max_tokens_per_session=rate_config.get("max_tokens_per_session", 100_000),
        )

    # ── Gate 1 + Gate 3 ──────────────────────────────────────────────────
    def guard_input(self, text: str):
        for pattern in self.content_filter_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                message = f"Blocked by Gate 1 (Content Filter): matched injection pattern '{pattern}'"
                self.audit.log(
                    "input_blocked", gate=1, query_preview=text[:80], reason=message
                )
                return False, message, "high"

        for pattern in self.policy_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                message = (
                    "Blocked by Gate 3 (Policy Check): this assistant is read-only. "
                    f"Requested action matches forbidden pattern '{pattern}'"
                )
                self.audit.log(
                    "input_blocked", gate=3, query_preview=text[:80], reason=message
                )
                return False, message, "high"

        return True, "ok", "low"

    # ── Gate 2 ───────────────────────────────────────────────────────────
    def _redact(self, text: str):
        labels_hit = []
        for label, pattern in self.pii_rules:
            text, count = re.subn(pattern, f"[REDACTED-{label}]", text, flags=re.IGNORECASE)
            if count:
                labels_hit.append(label)
        return text, labels_hit

    def guard_chunks(self, documents):
        for chunk_index, document in enumerate(documents):
            clean_text, labels_hit = self._redact(document.page_content)
            if labels_hit:
                document.page_content = clean_text
                self.events.append(
                    f"\U0001f6e1 Gate 2 — redacted {', '.join(labels_hit)} "
                    f"in chunk {chunk_index + 1} before the model saw it"
                )
                self.audit.log(
                    "chunk_redacted",
                    gate=2,
                    chunk_index=chunk_index,
                    findings=[{"type": label, "count": 1} for label in labels_hit],
                )
        return documents

    def guard_output(self, text: str) -> str:
        clean_text, labels_hit = self._redact(text)
        if labels_hit:
            self.events.append(
                f"\U0001f6e1 Gate 2 — redacted {', '.join(labels_hit)} "
                "from the answer before it was shown"
            )
            self.audit.log(
                "chunk_redacted",
                gate=2,
                chunk_index=0,
                findings=[{"type": label, "count": 1} for label in labels_hit],
            )
        return clean_text
