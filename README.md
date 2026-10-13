# RAG Training Kit

A standalone, shareable kit for learning Retrieval-Augmented Generation (RAG)
by building a real one — end to end, with your own OpenAI key, no toy
shortcuts. Hand this whole folder to anyone: it does not depend on any other
project on your machine.

**New here? Start with [SETUP_GUIDE.md](SETUP_GUIDE.md)** for step-by-step
install instructions. This file is the map of what's inside.

## What's inside

```
RAG-Training-Kit/
├── README.md                 <- you are here
├── SETUP_GUIDE.md             <- step-by-step setup + how to run everything
├── requirements.txt            <- pip install -r requirements.txt
├── pyproject.toml              <- lets you `pip install -e .` the package below
├── .env.example                 <- copy to .env, add your OpenAI key
├── data/
│   ├── hr_notes_demo.txt        <- tiny sample doc used by notebook 0
│   └── incident_story_demo.txt   <- tiny sample doc used by notebook 1
├── src/
│   └── rag_assistant/            <- the real, working RAG package (importable)
│       ├── config/               <- settings + guardrails.yaml rules
│       ├── ingestion/             <- document loaders (text/PDF/URL)
│       ├── pipeline/               <- chunking, embeddings, vector store, LLM, RAG chain
│       ├── guardrails/              <- the "Five Gates" safety engine
│       └── observability/            <- audit log, metrics, tracing
└── docs/
    ├── 1_Hands_On_RAG_Walkthrough.ipynb    <- start here: build a RAG pipeline step by step
    ├── SETUP_1_Hands_On_RAG_Walkthrough.md  <- section-by-section guide to notebook 1 specifically
    ├── 2_Visual_RAG_Explainer.ipynb         <- the same pipeline, explained with diagrams
    ├── 3_RAG_From_Scratch_Live.ipynb         <- deepest dive: from scratch, plus Traditional
    │                                            vs Advanced vs Agentic RAG, live
    ├── Guardrails_Live_Demo.ipynb             <- the safety layer, 5 tests, fully offline
    ├── rag_helpers.py                          <- small display helpers the notebooks import
    └── RAG_Complete_Training_Deck.pptx          <- companion slide deck (35 slides)
```

## What makes this "real" RAG, not a toy

Every notebook here calls the actual OpenAI API for embeddings and chat
completions -- there is no offline/practice/fake-answer mode. You need your
own `OPENAI_API_KEY` (see `.env.example`), and each notebook will stop with a
clear message if it can't find one, rather than silently faking a result.

The code in `src/rag_assistant/` is a small but genuine production-style RAG
package: real chunking (`langchain-text-splitters`), real embeddings
(`text-embedding-3-small`, 1,536 dimensions), a real vector store
(Chroma), a real retrieval + generation chain, and a real guardrail engine
(content filtering, PII redaction, policy checks, rate limiting, audit
logging) -- the same code shape you'd find powering a live app, just small
enough to read end to end in one sitting.

## Suggested order

1. `1_Hands_On_RAG_Walkthrough.ipynb` -- the full pipeline, one concept per cell.
2. `2_Visual_RAG_Explainer.ipynb` -- same ideas, more pictures, less code.
3. `3_RAG_From_Scratch_Live.ipynb` -- build it from first principles, then see
   Traditional RAG vs. Advanced RAG (query rewriting, hybrid search,
   reranking) vs. Agentic RAG (the model decides when and how to retrieve),
   with a live agentic demo.
4. `Guardrails_Live_Demo.ipynb` -- the safety layer, 5 tests, no key needed.
5. `5_RAG_Types_Clear_Examples.md` -- runnable examples for Naive,
   Advanced, Agentic, Graph, and Multimodal RAG.
6. `RAG_Complete_Training_Deck.pptx` -- optional companion slides covering
   the same material for a classroom/presentation setting.

## License / sharing

This kit was put together for internal training and is meant to be shared
freely with teammates or students. There's no proprietary data in it -- both
sample documents (`data/hr_notes_demo.txt`, `data/incident_story_demo.txt`)
are synthetic, made up for the guardrails/PII demos.
