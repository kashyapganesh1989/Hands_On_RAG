"""The full retrieve -> guard -> augment -> generate -> guard chain, wired
into one class so the notebooks (and the real app) can call `.run(question)`
and get back an answer plus a trace of what happened.
"""

from time import perf_counter


class RAGChain:
    def __init__(self, retriever, llm, prompt, engine, metrics=None, audit=None):
        self.retriever = retriever
        self.llm = llm
        self.prompt = prompt
        self.engine = engine
        self.metrics = metrics
        self.audit = audit

    def run(self, user_question: str):
        started = perf_counter()

        allowed, message, severity = self.engine.guard_input(user_question)
        if not allowed:
            trace = {"blocked": True, "reason": message, "severity": severity}
            if self.metrics is not None:
                self.metrics.record(
                    event="blocked",
                    question=user_question,
                    elapsed=perf_counter() - started,
                )
            return message, [], trace

        documents = self.engine.guard_chunks(self.retriever.invoke(user_question))
        context = "\n\n---\n\n".join(d.page_content for d in documents)
        messages = self.prompt.format_messages(context=context, input=user_question)

        raw_answer = self.llm.invoke(messages).content
        answer = self.engine.guard_output(raw_answer)

        elapsed = perf_counter() - started
        trace = {"blocked": False, "chunks": len(documents), "elapsed": elapsed}

        if self.metrics is not None:
            self.metrics.record(
                event="answered",
                question=user_question,
                elapsed=elapsed,
                chunks=len(documents),
            )
        if self.audit is not None:
            self.audit.log(
                "response_sent",
                trace_id=self.audit.new_trace_id(),
                query_preview=user_question[:80],
                chunks_used=len(documents),
                answer_preview=answer[:80],
            )
        return answer, documents, trace
