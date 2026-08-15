from collections.abc import Callable
from enum import Enum
from functools import partial

from .open_ai_translator import DEFAULT_MODEL, DEFAULT_RETRIES
from .open_ai_translator import translate as open_ai_translate


class Translator(str, Enum):
    openai = "openai"


def get_translator(
    translator: str,
    model: str = DEFAULT_MODEL,
    retries: int = DEFAULT_RETRIES,
) -> Callable[[list[str], str, str], list[str]]:
    available = ", ".join(member.value for member in Translator)
    if translator == Translator.openai:
        return partial(open_ai_translate, model=model, retries=retries)
    raise ValueError(f"Invalid translator {translator!r}. Available translators: {available}")
