"""Centralizar o carregamento e a validação das configurações."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_OPENAI_CHAT_MODEL = "gpt-4o-mini"
DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_CHROMA_PERSIST_DIRECTORY = Path("chroma_db")
DEFAULT_RETRIEVER_TOP_K = 4


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_chat_model: str = DEFAULT_OPENAI_CHAT_MODEL
    openai_embedding_model: str = DEFAULT_OPENAI_EMBEDDING_MODEL
    chroma_persist_directory: Path = DEFAULT_CHROMA_PERSIST_DIRECTORY
    retriever_top_k: int = DEFAULT_RETRIEVER_TOP_K


def load_settings(env_file: Path = Path(".env")) -> Settings:
    load_dotenv(env_file)

    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    retriever_top_k = os.getenv("RETRIEVER_TOP_K", str(DEFAULT_RETRIEVER_TOP_K))

    openai_api_key, retriever_top_k = validate_values(openai_api_key, retriever_top_k)

    return Settings(
        openai_api_key=openai_api_key,
        openai_chat_model=os.getenv("OPENAI_CHAT_MODEL", DEFAULT_OPENAI_CHAT_MODEL),
        openai_embedding_model=os.getenv(
            "OPENAI_EMBEDDING_MODEL", DEFAULT_OPENAI_EMBEDDING_MODEL
        ),
        chroma_persist_directory=Path(
            os.getenv("CHROMA_PERSIST_DIRECTORY", str(DEFAULT_CHROMA_PERSIST_DIRECTORY))
        ),
        retriever_top_k=retriever_top_k,
    )


def validate_values(
    openai_api_key_value: str, retriever_top_k_value: str
) -> tuple[str, int]:

    openai_api_key = openai_api_key_value.strip()
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is required.")

    try:
        retriever_top_k = int(retriever_top_k_value)
    except ValueError as error:
        raise ValueError("RETRIEVER_TOP_K must be a positive integer.") from error
    if retriever_top_k <= 0:
        raise ValueError("RETRIEVER_TOP_K must be a positive integer.")

    return openai_api_key, retriever_top_k
