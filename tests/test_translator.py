import time
from functools import partial
from json import dumps
from unittest.mock import MagicMock

from pytest import MonkeyPatch, raises

from doculingo.common.errors import TranslationError
from doculingo.common.settings import settings
from doculingo.common.translators import Translator, get_translator, open_ai_translator


def _mock_client(content: str) -> MagicMock:
    client = MagicMock()
    client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content=content))]
    )
    return client


def test_translate_success(monkeypatch: MonkeyPatch) -> None:
    client = _mock_client(dumps(["Hola", "Adiós"]))
    monkeypatch.setattr(open_ai_translator, "_get_client", lambda: client)

    result = open_ai_translator.translate(["Hello", "Bye"], "english", "spanish")

    assert result == ["Hola", "Adiós"]
    client.chat.completions.create.assert_called_once()


def test_translate_length_mismatch_raises_after_retries(
    monkeypatch: MonkeyPatch,
) -> None:
    sleeps: list[int] = []
    monkeypatch.setattr(time, "sleep", sleeps.append)
    client = _mock_client(dumps(["only one"]))
    monkeypatch.setattr(open_ai_translator, "_get_client", lambda: client)

    with raises(TranslationError):
        open_ai_translator.translate(["a", "b"], "spanish", "english", retries=2)

    assert client.chat.completions.create.call_count == 3
    assert sleeps == [1, 2]


def test_translate_persistent_failure_raises_translation_error(
    monkeypatch: MonkeyPatch,
) -> None:
    sleeps: list[int] = []
    monkeypatch.setattr(time, "sleep", sleeps.append)
    client = MagicMock()
    client.chat.completions.create.side_effect = RuntimeError("boom")
    monkeypatch.setattr(open_ai_translator, "_get_client", lambda: client)

    with raises(TranslationError, match="after 3 attempts") as exc_info:
        open_ai_translator.translate(["a"], "spanish", "english", retries=2)

    assert exc_info.value.__cause__ is not None
    assert client.chat.completions.create.call_count == 3
    assert sleeps == [1, 2]


def test_translate_missing_api_key(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "openai_api_key", None)
    open_ai_translator._get_client.cache_clear()

    try:
        with raises(RuntimeError, match="OPENAI_API_KEY"):
            open_ai_translator.translate(["a"], "spanish", "english")
    finally:
        open_ai_translator._get_client.cache_clear()


def test_get_translator_invalid_value() -> None:
    with raises(ValueError, match="deepl.*openai"):
        get_translator("deepl")


def test_get_translator_returns_openai_translator() -> None:
    translate = get_translator(Translator.openai)
    assert callable(translate)


def test_get_translator_forwards_model_and_retries() -> None:
    translate = get_translator("openai", model="gpt-4o-mini", retries=3)
    assert isinstance(translate, partial)
    assert translate.keywords == {"model": "gpt-4o-mini", "retries": 3}
