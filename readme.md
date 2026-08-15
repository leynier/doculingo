# DocuLingo

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/pypi/v/doculingo?color=%2334D058&label=Version)](https://pypi.org/project/doculingo)
[![Python versions](https://img.shields.io/pypi/pyversions/doculingo)](https://pypi.org/project/doculingo)
[![CI](https://github.com/leynier/doculingo/actions/workflows/tests.yml/badge.svg)](https://github.com/leynier/doculingo/actions/workflows/tests.yml)
[![Last commit](https://img.shields.io/github/last-commit/leynier/doculingo.svg?style=flat)](https://github.com/leynier/doculingo/commits)
[![Commit activity](https://img.shields.io/github/commit-activity/m/leynier/doculingo)](https://github.com/leynier/doculingo/commits)
[![Stars](https://img.shields.io/github/stars/leynier/doculingo?style=flat&logo=github)](https://github.com/leynier/doculingo/stargazers)
[![Forks](https://img.shields.io/github/forks/leynier/doculingo?style=flat&logo=github)](https://github.com/leynier/doculingo/network/members)
[![Watchers](https://img.shields.io/github/watchers/leynier/doculingo?style=flat&logo=github)](https://github.com/leynier/doculingo)
[![Contributors](https://img.shields.io/github/contributors/leynier/doculingo)](https://github.com/leynier/doculingo/graphs/contributors)

A **command-line tool** to translate large documents using language models. It preserves the file formatting and simplifies migrating documentation to other languages.

---

## Table of Contents

* [Overview](#overview)
* [Key Features](#key-features)
* [Installation](#installation)
* [Quick Start](#quick-start)
* [CLI Reference](#cli-reference)
* [Configuration](#configuration)
* [Limitations](#limitations)
* [Development](#development)
* [License](#license)

---

## Overview

`doculingo` helps you translate documents while preserving their formatting. It currently works with Word files and aims to support additional formats in the future, making it ideal for projects that require multiple language versions without losing the original layout.

---

## Key Features

* ✨ **Automatic Translation** — uses OpenAI to safely translate paragraphs.
* 📝 **Preserves Styles** — copies fonts, colors, and alignment to the translated version.
* 📄 **Document Support** — currently handles large `.docx` files with more formats planned.
* 🔁 **Automatic Retries** — retries with exponential backoff when the API fails and exits with a clear error if all retries fail.
* ⚙️ **Simple CLI** — clear commands with built-in help.

---

## Installation

Run instantly with [uv](https://github.com/astral-sh/uv) without installing:

```bash
uvx doculingo --help
```

Or install from PyPI:

```bash
pip install doculingo
```

---

## Quick Start

Translate a Word document from Spanish to English:

```bash
doculingo word \
  --input file.docx \
  --output translated.docx \
  --language-source spanish \
  --language-target english
```

---

## CLI Reference

Get the full list of options with:

```bash
doculingo --help
```

The main subcommand is `word`, designed for `.docx` files:

| Option | Required | Default | Description |
| --- | --- | --- | --- |
| `--input`, `-i` | Yes | — | Input `.docx` file path. |
| `--output`, `-o` | Yes | — | Output file path. The `.docx` suffix is appended if missing. |
| `--language-source`, `-s` | Yes | — | Source language. For example: `spanish`. |
| `--language-target`, `-t` | Yes | — | Target language. For example: `english`. |
| `--translator` | No | `openai` | Translator implementation. Only `openai` is available for now. |
| `--model` | No | `gpt-4o` | Model used by the translator. |
| `--retries` | No | `5` | Number of retries after the first failed translation attempt, with exponential backoff. |

Example using a different model and fewer retries:

```bash
doculingo word \
  --input file.docx \
  --output translated.docx \
  --language-source spanish \
  --language-target english \
  --model gpt-4o-mini \
  --retries 3
```

---

## Configuration

`doculingo` reads configuration from environment variables (a local `.env` file is also supported). Copy `.env.example` to `.env` and fill in your values:

| Variable | Required | Description |
| --- | --- | --- |
| `OPENAI_API_KEY` | Yes | OpenAI API key used by the OpenAI translator. Get one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys). |

The model can be selected per run with `--model`; it defaults to `gpt-4o`.

---

## Limitations

* Only top-level document paragraphs are translated. Content inside **tables**, **headers and footers**, and paragraphs inside **shapes** (text boxes, SmartArt) is not translated.
* Paragraphs made of **multiple runs** (mixed formatting within a paragraph) are translated as a whole, so their internal formatting is collapsed into a single run in the output document.
* The output document is rebuilt from paragraphs only, so other document parts such as images and tables are not carried over.

---

## Development

Install the dependencies and run the tool locally:

```bash
uv lock
uv sync --all-groups --all-extras
uv run doculingo --help
```

Common tasks are available through the `makefile`:

```bash
make install     # uv sync --all-groups --all-extras
make format      # ruff format
make lint        # ruff check
make type-check  # mypy doculingo
make test        # pytest
```

---

## License

Distributed under the MIT license. See the [`license`](license) file.
