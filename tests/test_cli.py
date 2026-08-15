from pathlib import Path

from docx import Document
from pytest import MonkeyPatch
from typer.testing import CliRunner

from doculingo import word
from doculingo.common.errors import TranslationError
from doculingo.main import app

runner = CliRunner()


def test_help_without_api_key(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "word" in result.output


def test_word_help_without_api_key(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = runner.invoke(app, ["word", "--help"], env={"COLUMNS": "200"})
    assert result.exit_code == 0
    assert "--model" in result.output
    assert "--retries" in result.output


def test_word_translation_error_exits_non_zero(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    def failing_translate(items: list[str], ls: str, lt: str) -> list[str]:
        raise TranslationError("translation failed")

    monkeypatch.setattr(word, "get_translator", lambda *a, **k: failing_translate)

    doc = Document()
    doc.add_paragraph("hola")
    input_file = tmp_path / "input.docx"
    doc.save(str(input_file))

    result = runner.invoke(
        app,
        [
            "word",
            "--input",
            str(input_file),
            "--output",
            str(tmp_path / "output.docx"),
            "--language-source",
            "spanish",
            "--language-target",
            "english",
        ],
    )

    assert result.exit_code == 1
    assert "translation failed" in result.output + result.stderr


def test_word_rejects_non_docx_input(tmp_path: Path) -> None:
    input_file = tmp_path / "input.txt"
    input_file.write_text("not a docx")

    result = runner.invoke(
        app,
        [
            "word",
            "--input",
            str(input_file),
            "--output",
            str(tmp_path / "output.docx"),
            "--language-source",
            "spanish",
            "--language-target",
            "english",
        ],
    )

    assert result.exit_code == 2
    assert ".docx" in result.output + result.stderr
