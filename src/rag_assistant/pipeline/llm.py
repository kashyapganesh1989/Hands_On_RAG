"""The model + prompt used for generation. The entire "grounding" rule this
project relies on lives in the system prompt below: answer only from the
supplied context, and say so plainly when the answer isn't there.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from rag_assistant.config.settings import settings


def build_llm_and_prompt(api_key: str):
    llm = ChatOpenAI(
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
        openai_api_key=api_key,
    )
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Use ONLY the provided context to answer. If the answer is not "
            "in the context, say so.\n\nContext:\n{context}",
        ),
        ("human", "{input}"),
    ])
    return llm, prompt
