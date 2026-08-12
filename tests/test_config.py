from pathlib import Path

from src import config


def test_load_settings_uses_defaults(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
    monkeypatch.delenv("OPENAI_CHAT_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_EMBEDDING_MODEL", raising=False)
    monkeypatch.delenv("CHROMA_PERSIST_DIRECTORY", raising=False)
    monkeypatch.delenv("RETRIEVER_TOP_K", raising=False)

    settings = config.load_settings(tmp_path / ".env")
    assert settings.openai_api_key == "test_api_key", (
        "openai_api_key is different from the default"
    )
    assert settings.openai_chat_model == config.DEFAULT_OPENAI_CHAT_MODEL, (
        "openai_chat_model is different from the default"
    )
    assert settings.openai_embedding_model == config.DEFAULT_OPENAI_EMBEDDING_MODEL, (
        "openai_embedding_model is different from the default"
    )
    assert (
        settings.chroma_persist_directory == config.DEFAULT_CHROMA_PERSIST_DIRECTORY
    ), "chroma_persist_directory is different from the default"
    assert settings.retriever_top_k == config.DEFAULT_RETRIEVER_TOP_K, (
        "retriever_top_k is different from the default"
    )


def test_load_settings_from_env_file(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_CHAT_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_EMBEDDING_MODEL", raising=False)
    monkeypatch.delenv("CHROMA_PERSIST_DIRECTORY", raising=False)
    monkeypatch.delenv("RETRIEVER_TOP_K", raising=False)

    env_file = tmp_path / ".env"
    env_file.write_text(
        "OPENAI_API_KEY = custom_test_api_key\n"
        "OPENAI_CHAT_MODEL = custom-chat-model\n"
        "OPENAI_EMBEDDING_MODEL = custom-embedding-model\n"
        "CHROMA_PERSIST_DIRECTORY = custom-chroma_persist_directory\n"
        "RETRIEVER_TOP_K = 89\n",
        encoding="utf-8",
    )
    settings = config.load_settings(env_file)

    assert settings.openai_api_key == "custom_test_api_key", (
        "openai_api_key is different from the .env file"
    )
    assert settings.openai_chat_model == "custom-chat-model", (
        "openai_chat_model is different from the .env file"
    )
    assert settings.openai_embedding_model == "custom-embedding-model", (
        "openai_embedding_model is different from the .env file"
    )
    assert settings.chroma_persist_directory == Path(
        "custom-chroma_persist_directory"
    ), "chroma_persist_directory is different from the .env file"
    assert settings.retriever_top_k == 89, (
        "retriever_top_k is different from the .env file"
    )


# No próximo cenário, será testada a ausência da variável `OPENAI_API_KEY`.
# O teste deverá confirmar que a função `load_settings()` lança um `ValueError` contendo a mensagem esperada.
# Para realizar essa validação, utilizaremos o `pytest.raises`,
# que desempenha um papel equivalente ao `expectException()` do PHPUnit.
