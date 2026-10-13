"""Gate 5 — the tamper-proof audit log.

Every entry stores a hash of itself computed over its own fields plus the
hash of the entry before it — a simple hash chain, like a wax seal. Editing
any old entry, even by a single character, changes what its stored hash
should have been, and `verify_chain()` catches that on the very next check.
"""

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

GENESIS = "GENESIS"


class AuditLogger:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()

    @staticmethod
    def new_trace_id() -> str:
        return uuid.uuid4().hex[:12]

    def _last_hash(self) -> str:
        lines = self.path.read_text(encoding="utf-8").splitlines()
        if not lines:
            return GENESIS
        try:
            return json.loads(lines[-1]).get("hash", GENESIS)
        except json.JSONDecodeError:
            return GENESIS

    @staticmethod
    def _compute_hash(payload: dict) -> str:
        body = json.dumps(payload, sort_keys=True, default=str)
        return hashlib.sha256(body.encode("utf-8")).hexdigest()

    def log(self, event: str, **fields):
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "prev_hash": self._last_hash(),
            **fields,
        }
        record = {**payload, "hash": self._compute_hash(payload)}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        return record

    def verify_chain(self):
        """Walk the log from the start, recomputing each entry's hash.
        Returns (True, total_records) if every entry checks out, or
        (False, records_verified_before_the_break) at the first mismatch.
        """
        lines = self.path.read_text(encoding="utf-8").splitlines()
        prev_hash = GENESIS

        for i, line in enumerate(lines):
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                return False, i

            stored_hash = record.get("hash")
            payload = {k: v for k, v in record.items() if k != "hash"}

            if payload.get("prev_hash") != prev_hash:
                return False, i
            if stored_hash != self._compute_hash(payload):
                return False, i

            prev_hash = stored_hash

        return True, len(lines)
