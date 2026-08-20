"""Routes every agent in this app through OpenRouter instead of OpenAI directly.

OpenRouter only speaks the Chat Completions format (no Responses API, no OpenAI-hosted
tools), so we point the SDK's default OpenAI client at OpenRouter's base URL and force
chat_completions mode. Tracing is disabled since it uploads to OpenAI's own platform,
which needs a real OpenAI API key we don't have here.
"""

import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import set_default_openai_api, set_default_openai_client, set_tracing_disabled

load_dotenv(override=True)

MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "openai/gpt-4.1-mini")

_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
set_default_openai_client(_client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)
