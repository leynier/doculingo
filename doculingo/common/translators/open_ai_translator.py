import logging
import time
from functools import lru_cache
from json import dumps, loads

from openai import OpenAI
from openai.types import ChatModel
from openai.types.chat import ChatCompletionMessageParam

from ..errors import TranslationError
from ..settings import settings

logger = logging.getLogger(__name__)

DEFAULT_MODEL: ChatModel = "gpt-4o"
DEFAULT_RETRIES = 5
_MAX_BACKOFF_SECONDS = 60


@lru_cache(maxsize=1)
def _get_client() -> OpenAI:
    api_key = settings.openai_api_key
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Export it as an environment variable or add it "
            "to a .env file in the working directory (see .env.example) to use the "
            "OpenAI translator."
        )
    return OpenAI(api_key=api_key)


def translate(
    texts: list[str],
    language_source: str,
    language_target: str,
    model: str = DEFAULT_MODEL,
    retries: int = DEFAULT_RETRIES,
) -> list[str]:
    client = _get_client()
    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": f"""
                You are an expert translator from {language_source} to {language_target}.
                Everything the user writes should simply be translated into {language_target}.
                The user will send a JSON with a list of texts, and the response should
                be another JSON with the list of translations.

                For example, a translation from Spanish to English would look like this:

                Input example: ["Hola, ¿cómo estás?", "Estoy bien, gracias."]
                Output example: ["Hello, how are you?", "I'm fine, thank you."]
            """,
        },
        {
            "role": "user",
            "content": dumps(texts),
        },
    ]
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            logger.info(
                "Translating %d texts (attempt %d of %d)", len(texts), attempt + 1, retries + 1
            )
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": "json_object"},
            )
            if not response.choices or not response.choices[0].message.content:
                raise ValueError("The API response has no content")
            result = loads(response.choices[0].message.content)
            if isinstance(result, dict):
                result = list(result.values())
            if isinstance(result, list) and len(result) == 1 and isinstance(result[0], list):
                result = result[0]
            if (
                not isinstance(result, list)
                or len(result) != len(texts)
                or any(not isinstance(text, str) for text in result)
            ):
                raise ValueError(
                    f"The API response does not match the input: "
                    f"expected a list of {len(texts)} strings"
                )
            logger.info("Translated %d texts successfully (attempt %d)", len(texts), attempt + 1)
            return result
        except Exception as error:  # noqa: BLE001
            last_error = error
            logger.warning(
                "Translation attempt %d of %d failed: %s",
                attempt + 1,
                retries + 1,
                error,
            )
            if attempt < retries:
                delay = min(2**attempt, _MAX_BACKOFF_SECONDS)
                logger.warning("Retrying in %d seconds...", delay)
                time.sleep(delay)
    raise TranslationError(
        f"Failed to translate {len(texts)} texts from "
        f"{language_source} to {language_target} after {retries + 1} attempts"
    ) from last_error
