# Five RAG Types: Clear Examples

This guide shows five common RAG implementation styles with runnable examples
from `rag_assistant.pipeline.rag_patterns`. The examples use a tiny in-memory
retriever and deterministic demo LLM so they run without an API key. In a real
app, replace those pieces with embeddings, a vector database, graph storage, and
your production chat model.

Run all examples:

```bash
python -m rag_assistant.pipeline.rag_patterns
```

Or from Python:

```python
from rag_assistant.pipeline.rag_patterns import run_all_examples

results = run_all_examples()
print(results["naive"]["answer"])
```

## 1. Naive / Traditional RAG

**Pattern:** retrieve once, place the top chunks in the prompt, generate an
answer.

**Best for:** first prototypes, simple Q&A over well-structured text, and
teaching the core retrieve -> augment -> generate flow.

**Limit:** the first retrieved chunks must be good, because there is no query
rewriting, reranking, decomposition, or tool planning.

```python
from rag_assistant.pipeline.rag_patterns import (
    KeywordRetriever,
    demo_corpus,
    naive_rag,
)

retriever = KeywordRetriever(demo_corpus())
result = naive_rag("What is naive RAG?", retriever)

print(result["answer"])
print([chunk.source for chunk in result["chunks"]])
```

Implementation shape:

```text
question -> retrieve top-k chunks -> prompt with context -> answer
```

## 2. Advanced RAG

**Pattern:** improve retrieval quality before generation. The example uses query
rewriting, multi-query retrieval, deduplication, reranking, and compression.

**Best for:** production Q&A where wording varies, documents overlap, or top-k
retrieval is noisy.

**Limit:** more moving parts means more evaluation is needed. Track whether each
step improves answer quality on real questions.

```python
from rag_assistant.pipeline.rag_patterns import (
    KeywordRetriever,
    advanced_rag,
    demo_corpus,
)

retriever = KeywordRetriever(demo_corpus())
result = advanced_rag("How does advanced RAG improve retrieval?", retriever)

print(result["rewritten_queries"])
print(result["answer"])
```

Implementation shape:

```text
question
  -> rewrite into several search queries
  -> retrieve candidates
  -> dedupe and rerank
  -> compress context
  -> answer
```

## 3. Agentic RAG

**Pattern:** an agent decides which retrieval actions to take, inspects what came
back, and stops when it has enough evidence.

**Best for:** complex questions that may need multiple tools, comparisons,
decomposition, or follow-up retrieval.

**Limit:** agentic systems need guardrails, tracing, timeouts, and tool budgets
because they can over-search or choose poor actions.

```python
from rag_assistant.pipeline.rag_patterns import (
    KeywordRetriever,
    agentic_rag,
    demo_corpus,
)

retriever = KeywordRetriever(demo_corpus())
result = agentic_rag("Compare agentic RAG and naive RAG risks.", retriever)

print(result["trace"])
print(result["answer"])
```

Implementation shape:

```text
question
  -> decide action
  -> retrieve with selected query/tool
  -> inspect evidence
  -> optionally retrieve again
  -> final grounded answer
```

## 4. Graph RAG

**Pattern:** retrieve from a graph of entities and relationships, then answer
from the connected facts.

**Best for:** questions about relationships, dependencies, lineage, ownership,
multi-hop reasoning, or "how is X connected to Y?"

**Limit:** graph quality matters. You need reliable entity extraction,
deduplication, relationship extraction, and graph updates.

```python
from rag_assistant.pipeline.rag_patterns import (
    GraphEdge,
    MiniKnowledgeGraph,
    graph_rag,
)

graph = MiniKnowledgeGraph([
    GraphEdge("RAG", "has_pattern", "Advanced RAG", "graph#1"),
    GraphEdge("Advanced RAG", "uses", "reranking", "graph#2"),
    GraphEdge("Advanced RAG", "uses", "query rewriting", "graph#3"),
    GraphEdge("RAG", "has_pattern", "Graph RAG", "graph#4"),
    GraphEdge("Graph RAG", "uses", "entity relationships", "graph#5"),
])

result = graph_rag(
    "How does Graph RAG use relationships?",
    graph,
    seed_entities=["RAG"],
)

print(result["entities"])
print(result["answer"])
```

Implementation shape:

```text
question
  -> extract seed entities
  -> traverse graph neighborhood
  -> turn facts into grounded context
  -> answer with citations
```

## 5. Multimodal RAG

**Pattern:** retrieve across text and non-text assets such as images, diagrams,
OCR, tables, audio transcripts, or video metadata.

**Best for:** manuals with diagrams, slide decks, screenshots, scanned forms,
catalogs, training videos, and inspection workflows.

**Limit:** the retrieval index needs useful representations of each modality.
For images, that usually means captions, OCR, visual embeddings, or all three.

```python
from rag_assistant.pipeline.rag_patterns import (
    ImageAsset,
    demo_corpus,
    multimodal_rag,
)

images = [
    ImageAsset(
        image_id="architecture-01",
        caption="A diagram showing text and image embeddings flowing into one retrieval index.",
        ocr_text="multimodal RAG shared index",
        source="slides#multimodal-diagram",
    )
]

result = multimodal_rag(
    "How does multimodal RAG use diagrams?",
    demo_corpus(),
    images,
)

print(result["answer"])
print([chunk.metadata for chunk in result["chunks"]])
```

Implementation shape:

```text
text docs + image captions/OCR/visual embeddings
  -> shared or hybrid retrieval
  -> modality-aware context
  -> answer grounded in retrieved text and media evidence
```

## Quick Comparison

| Type | Retrieval behavior | Extra ingredient | Good first use case |
| --- | --- | --- | --- |
| Naive / Traditional RAG | One top-k retrieval pass | None | Basic document Q&A |
| Advanced RAG | Better search before answering | Rewrite, rerank, compress | Noisy enterprise docs |
| Agentic RAG | Model chooses retrieval steps | Tool planning and traces | Complex multi-step tasks |
| Graph RAG | Traverses entity relationships | Knowledge graph | Multi-hop relationship Q&A |
| Multimodal RAG | Searches text plus media evidence | Captions, OCR, visual embeddings | Diagrams, screenshots, forms |

