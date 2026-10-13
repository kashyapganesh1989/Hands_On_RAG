"""Tracing — one trace per query, one span per pipeline step.

Answers the only diagnostic question that matters when an answer goes wrong:
was it the FINDING (retrieval) or the ANSWERING (generation) that broke?
Mirrors the OpenTelemetry span model in miniature, with zero dependencies."""

import time
import uuid
from contextlib import contextmanager


class Trace:
    def __init__(self):
        self.trace_id = uuid.uuid4().hex[:12]
        self.spans: dict[str, float] = {}

    @contextmanager
    def span(self, name: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            self.spans[name] = (time.perf_counter() - start) * 1000  # ms

    def ms(self, name: str) -> float:
        return self.spans.get(name, 0.0)
