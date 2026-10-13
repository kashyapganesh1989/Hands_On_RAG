"""Lightweight metrics collection — one JSON line per event, for later
analysis (latency, chunk counts, block rate). Not tamper-evident like the
audit log; this is operational telemetry, not a compliance record.
"""

import json
from datetime import datetime, timezone
from pathlib import Path


class MetricsCollector:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()

    def record(self, event: str, **fields):
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event": event,
            **fields,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        return entry
