"""Chunking, embedding, and vector storage in one call."""

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag_assistant.config.settings import settings


def build_vectorstore(docs, api_key: str):
    """Split docs into chunks, embed them, and return (retriever, n_chunks)."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_documents(docs)

    embedding_model = OpenAIEmbeddings(
        openai_api_key=api_key,
        model="text-embedding-3-small",
    )
    vector_store = Chroma.from_documents(documents=chunks, embedding=embedding_model)
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": settings.retriever_k},
    )
    return retriever, len(chunks)
