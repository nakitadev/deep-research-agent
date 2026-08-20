"""Routes every agent in this app through OpenRouter instead of OpenAI directly.

OpenRouter only speaks the Chat Completions format (no Responses API, no OpenAI-hosted
tools), so we point the SDK's default OpenAI client at OpenRouter's base URL and force
chat_completions mode.

Tracing is a separate concern from model routing: the SDK's trace/span data still
describes agent workflow steps regardless of which provider serves the actual model
calls, but the built-in exporter uploads that data to OpenAI's own tracing platform and
needs a real OpenAI API key to authenticate the upload (no OpenAI model calls happen).
Set OPENAI_API_KEY to see traces at https://platform.openai.com/traces; leave it unset
to disable tracing entirely.
"""

import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import (
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
    set_tracing_export_api_key,
)

load_dotenv(override=True)

MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "openai/gpt-4.1-mini")

_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
set_default_openai_client(_client, use_for_tracing=False)
set_default_openai_api("chat_completions")

_tracing_key = os.getenv("OPENAI_API_KEY")
TRACING_ENABLED = bool(_tracing_key)
if TRACING_ENABLED:
    set_tracing_export_api_key(_tracing_key)
else:
    set_tracing_disabled(True)
