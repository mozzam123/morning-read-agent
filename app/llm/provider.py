from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import ChatOllama

from app.core.config import settings


def get_llm() -> BaseChatModel:

    if settings.llm_provider == "ollama":
        return ChatOllama(
            model=settings.llm_model,
            temperature=0,
        )

    if settings.llm_provider == "groq":
        return _get_groq_llm()

    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")


def _get_groq_llm() -> BaseChatModel:
    try:
        from langchain_groq import ChatGroq
    except ImportError as exc:
        raise RuntimeError(
            "Groq provider requires 'langchain-groq'. "
            "Install it with: pip install langchain-groq"
        ) from exc

    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY is required when using Groq.")

    return ChatGroq(
        model=settings.llm_model,
        api_key=settings.groq_api_key,
        temperature=0,
    )
