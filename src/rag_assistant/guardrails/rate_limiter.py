"""Gate 4 — Rate Limiter. A per-session cap on both request count and
estimated token usage, so a bug or an abusive session can't run up a huge
bill. Deliberately simple: an in-memory counter, reset per process/session.
"""


def _estimate_tokens(text: str) -> int:
    """Rough, fast token estimate (~4 characters per token). Good enough for
    a budget guard — not meant to match the real tokenizer exactly."""
    return max(1, len(text) // 4)


class RateLimiter:
    def __init__(self, max_calls_per_session: int = 10, max_tokens_per_session: int = 100_000):
        self.max_calls = max_calls_per_session
        self.max_tokens = max_tokens_per_session
        self.calls = []
        self.tokens_used = 0

    def allow(self, text: str):
        if len(self.calls) >= self.max_calls:
            return False, (
                f"Blocked by Gate 4 (Rate Limiter): session call cap reached "
                f"({len(self.calls)}/{self.max_calls}). Graceful stop — not a $15,000 invoice."
            )

        if _estimate_tokens(text) > (self.max_tokens - self.tokens_used):
            return False, (
                f"Blocked by Gate 4 (Rate Limiter): session token budget reached "
                f"({self.tokens_used}/{self.max_tokens} used). Graceful stop."
            )

        return True, "within budget"

    def record(self, question: str, answer: str):
        self.calls.append((question, answer))
        self.tokens_used += _estimate_tokens(question) + _estimate_tokens(answer)
