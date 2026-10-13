"""Clear, dependency-light examples of common RAG patterns.

These examples are intentionally small enough to read in a workshop, but each
one mirrors the production shape of the pattern it demonstrates. They use an
in-memory keyword retriever and a deterministic demo LLM so they can run without
an API key. Swap those two pieces for embeddings, a vector database, and a real
chat model when moving from training to production.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
import re
from typing import Callable, Iterable


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "what",
    "when",
    "where",
    "which",
    "with",
}


@dataclass(frozen=True)
class Chunk:
    """A retrieved unit of context."""

    text: str
    source: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ImageAsset:
    """Tiny stand-in for an image plus the text a multimodal index stores."""

    image_id: str
    caption: str
    ocr_text: str = ""
    source: str = "image"


@dataclass(frozen=True)
class GraphEdge:
    """A fact edge used by the Graph RAG example."""

    subject: str
    relation: str
    object: str
    source: str


def tokenize(text: str) -> set[str]:
    """Lowercase keyword tokens used by the demo retrievers and reranker."""

    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in STOPWORDS and len(token) > 1
    }


class KeywordRetriever:
    """Simple retriever with the same shape as a vector-store retriever."""

    def __init__(self, chunks: Iterable[Chunk]):
        self.chunks = list(chunks)

    def retrieve(self, query: str, k: int = 3) -> list[Chunk]:
        query_terms = tokenize(query)
        scored = []
        for chunk in self.chunks:
            chunk_terms = tokenize(chunk.text)
            score = len(query_terms & chunk_terms)
            if score:
                scored.append((score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[:k]]


def demo_llm(question: str, context: Iterable[Chunk]) -> str:
    """Deterministic replacement for an LLM in the training examples."""

    chunks = list(context)
    if not chunks:
        return "I do not have enough retrieved context to answer."

    citations = ", ".join(chunk.source for chunk in chunks)
    evidence = " ".join(chunk.text for chunk in chunks[:2])
    return f"Answer grounded in {citations}: {evidence}"


def _dedupe_chunks(chunks: Iterable[Chunk]) -> list[Chunk]:
    seen = set()
    unique = []
    for chunk in chunks:
        key = (chunk.source, chunk.text)
        if key not in seen:
            unique.append(chunk)
            seen.add(key)
    return unique


def _rerank(question: str, chunks: Iterable[Chunk]) -> list[Chunk]:
    question_terms = tokenize(question)
    return sorted(
        chunks,
        key=lambda chunk: len(question_terms & tokenize(chunk.text)),
        reverse=True,
    )


def _compress(chunk: Chunk, question: str, max_sentences: int = 2) -> Chunk:
    question_terms = tokenize(question)
    sentences = re.split(r"(?<=[.!?])\s+", chunk.text)
    ranked = sorted(
        sentences,
        key=lambda sentence: len(question_terms & tokenize(sentence)),
        reverse=True,
    )
    text = " ".join(sentence for sentence in ranked[:max_sentences] if sentence)
    return Chunk(text=text or chunk.text, source=chunk.source, metadata=chunk.metadata)


def naive_rag(
    question: str,
    retriever: KeywordRetriever,
    llm: Callable[[str, Iterable[Chunk]], str] = demo_llm,
    k: int = 3,
) -> dict[str, object]:
    """Naive RAG: retrieve once, stuff top chunks into the prompt, answer."""

    chunks = retriever.retrieve(question, k=k)
    answer = llm(question, chunks)
    return {"pattern": "naive_rag", "answer": answer, "chunks": chunks}


def advanced_rag(
    question: str,
    retriever: KeywordRetriever,
    llm: Callable[[str, Iterable[Chunk]], str] = demo_llm,
    k: int = 3,
) -> dict[str, object]:
    """Advanced RAG: rewrite, multi-query retrieve, rerank, compress, answer."""

    rewritten_queries = [
        question,
        f"{question} policy process requirements",
        f"{question} risk exception owner",
    ]
    candidates = []
    for query in rewritten_queries:
        candidates.extend(retriever.retrieve(query, k=k))

    reranked = _rerank(question, _dedupe_chunks(candidates))
    compressed = [_compress(chunk, question) for chunk in reranked[:k]]
    answer = llm(question, compressed)
    return {
        "pattern": "advanced_rag",
        "rewritten_queries": rewritten_queries,
        "answer": answer,
        "chunks": compressed,
    }


def agentic_rag(
    question: str,
    retriever: KeywordRetriever,
    llm: Callable[[str, Iterable[Chunk]], str] = demo_llm,
    max_steps: int = 3,
) -> dict[str, object]:
    """Agentic RAG: choose retrieval actions, inspect evidence, then answer."""

    plan = ["retrieve_direct"]
    if any(word in question.lower() for word in ("compare", "difference", "vs")):
        plan.append("retrieve_comparison")
    if any(word in question.lower() for word in ("risk", "why", "explain")):
        plan.append("retrieve_risk")

    evidence = []
    trace = []
    for step, action in enumerate(plan[:max_steps], start=1):
        if action == "retrieve_direct":
            query = question
        elif action == "retrieve_comparison":
            query = f"{question} compare tradeoffs"
        else:
            query = f"{question} risk cause mitigation"

        found = retriever.retrieve(query, k=2)
        evidence.extend(found)
        trace.append({"step": step, "action": action, "query": query, "chunks": len(found)})
        if len(_dedupe_chunks(evidence)) >= 3:
            break

    final_evidence = _dedupe_chunks(evidence)
    answer = llm(question, final_evidence)
    return {
        "pattern": "agentic_rag",
        "trace": trace,
        "answer": answer,
        "chunks": final_evidence,
    }


class MiniKnowledgeGraph:
    """Small in-memory graph for showing Graph RAG traversal."""

    def __init__(self, edges: Iterable[GraphEdge]):
        self.edges = list(edges)
        self.by_subject: dict[str, list[GraphEdge]] = defaultdict(list)
        for edge in self.edges:
            self.by_subject[edge.subject.lower()].append(edge)

    def neighborhood(self, entity: str, hops: int = 2) -> list[GraphEdge]:
        visited = set()
        results = []
        queue = deque([(entity.lower(), 0)])
        while queue:
            node, depth = queue.popleft()
            if depth >= hops:
                continue
            for edge in self.by_subject.get(node, []):
                key = (edge.subject, edge.relation, edge.object)
                if key in visited:
                    continue
                visited.add(key)
                results.append(edge)
                queue.append((edge.object.lower(), depth + 1))
        return results


def graph_rag(
    question: str,
    graph: MiniKnowledgeGraph,
    llm: Callable[[str, Iterable[Chunk]], str] = demo_llm,
    seed_entities: Iterable[str] | None = None,
) -> dict[str, object]:
    """Graph RAG: find entities, traverse relationships, answer with facts."""

    entities = list(seed_entities or [])
    if not entities:
        question_terms = tokenize(question)
        entities = [
            edge.subject
            for edge in graph.edges
            if edge.subject.lower() in question_terms or edge.object.lower() in question_terms
        ]
    if not entities and graph.edges:
        entities = [graph.edges[0].subject]

    facts = []
    for entity in entities:
        facts.extend(graph.neighborhood(entity, hops=2))

    chunks = [
        Chunk(
            text=f"{edge.subject} {edge.relation} {edge.object}.",
            source=edge.source,
            metadata={"subject": edge.subject, "relation": edge.relation, "object": edge.object},
        )
        for edge in facts
    ]
    answer = llm(question, chunks)
    return {"pattern": "graph_rag", "entities": entities, "answer": answer, "chunks": chunks}


def multimodal_rag(
    question: str,
    text_chunks: Iterable[Chunk],
    images: Iterable[ImageAsset],
    llm: Callable[[str, Iterable[Chunk]], str] = demo_llm,
    k: int = 4,
) -> dict[str, object]:
    """Multimodal RAG: retrieve from text plus image captions/OCR, then answer."""

    image_chunks = [
        Chunk(
            text=f"Image {image.image_id}: {image.caption} {image.ocr_text}".strip(),
            source=image.source,
            metadata={"modality": "image", "image_id": image.image_id},
        )
        for image in images
    ]
    retriever = KeywordRetriever([*text_chunks, *image_chunks])
    chunks = retriever.retrieve(question, k=k)
    answer = llm(question, chunks)
    return {"pattern": "multimodal_rag", "answer": answer, "chunks": chunks}


def demo_corpus() -> list[Chunk]:
    """Reusable mini corpus for the examples and documentation."""

    return [
        Chunk(
            "Naive RAG retrieves the top matching chunks once and sends them to the model.",
            "rag-guide#naive",
        ),
        Chunk(
            "Advanced RAG improves retrieval with query rewriting, reranking, and context compression.",
            "rag-guide#advanced",
        ),
        Chunk(
            "Agentic RAG lets an agent choose when to retrieve, which tool to call, and when it has enough evidence.",
            "rag-guide#agentic",
        ),
        Chunk(
            "Graph RAG stores entities and relationships so answers can follow connected facts across multiple hops.",
            "rag-guide#graph",
        ),
        Chunk(
            "Multimodal RAG indexes text, image captions, OCR, tables, audio transcripts, or video metadata together.",
            "rag-guide#multimodal",
        ),
        Chunk(
            "Reranking checks candidate chunks against the question after retrieval and keeps the strongest evidence.",
            "rag-guide#reranking",
        ),
    ]


def run_all_examples() -> dict[str, dict[str, object]]:
    """Run one compact example of each RAG pattern."""

    retriever = KeywordRetriever(demo_corpus())
    graph = MiniKnowledgeGraph(
        [
            GraphEdge("RAG", "has_pattern", "Advanced RAG", "graph#1"),
            GraphEdge("Advanced RAG", "uses", "reranking", "graph#2"),
            GraphEdge("Advanced RAG", "uses", "query rewriting", "graph#3"),
            GraphEdge("RAG", "has_pattern", "Graph RAG", "graph#4"),
            GraphEdge("Graph RAG", "uses", "entity relationships", "graph#5"),
        ]
    )
    images = [
        ImageAsset(
            image_id="architecture-01",
            caption="A diagram showing text and image embeddings flowing into one retrieval index.",
            ocr_text="multimodal RAG shared index",
            source="slides#multimodal-diagram",
        )
    ]

    return {
        "naive": naive_rag("What is naive RAG?", retriever),
        "advanced": advanced_rag("How does advanced RAG improve retrieval?", retriever),
        "agentic": agentic_rag("Compare agentic RAG and naive RAG risks.", retriever),
        "graph": graph_rag("How does Graph RAG use relationships?", graph, seed_entities=["RAG"]),
        "multimodal": multimodal_rag(
            "How does multimodal RAG use diagrams?",
            demo_corpus(),
            images,
        ),
    }


if __name__ == "__main__":
    for name, result in run_all_examples().items():
        print(f"\n{name.upper()}")
        print(result["answer"])
