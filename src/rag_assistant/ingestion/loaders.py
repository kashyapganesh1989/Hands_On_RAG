"""Document loaders — the project's four "front doors" for getting documents
into the pipeline. Every loader returns the same shape: (docs, names), where
docs is a list of LangChain Document objects and names is a list of source
labels. Everything downstream (chunking, embedding, retrieval) works
identically no matter which door a document came through.
"""

from langchain_core.documents import Document


def load_text(text: str, label: str):
    """Wrap a raw string as a single Document."""
    return [Document(page_content=text, metadata={"source": label})], [label]


def load_pdf(path):
    """Load a local PDF, one Document per page."""
    from langchain_community.document_loaders import PyPDFLoader

    docs = PyPDFLoader(str(path)).load()
    names = [f"{path}#page={d.metadata.get('page', i)}" for i, d in enumerate(docs)]
    return docs, names


def load_url(urls):
    """Load one or more web pages."""
    from langchain_community.document_loaders import WebBaseLoader

    urls = [urls] if isinstance(urls, str) else list(urls)
    docs = WebBaseLoader(urls).load()
    return docs, urls


def load_db(query: str, connection_string: str):
    """Load rows from a SQL database via a query."""
    from langchain_community.document_loaders import SQLDatabaseLoader
    from langchain_community.utilities import SQLDatabase

    db = SQLDatabase.from_uri(connection_string)
    docs = SQLDatabaseLoader(query=query, db=db).load()
    names = [f"db-row-{i}" for i in range(len(docs))]
    return docs, names
