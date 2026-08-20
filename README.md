# deep-research-agent

A multi-agent deep research pipeline built on the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python),
routed through [OpenRouter](https://openrouter.ai) instead of OpenAI directly. Give it a
question, and four agents run in sequence: plan a set of web searches, run them in
parallel, write a long-form markdown report from the results, then email it to you.

## How it works

1. **Planner** — turns your query into N search terms with reasoning (`planner_agent.py`)
2. **Search** — runs each search via the Serper API and summarizes the results, in parallel (`search_agent.py`)
3. **Writer** — synthesizes all the summaries into a full markdown report, 1000+ words (`writer_agent.py`)
4. **Email** — formats the report as HTML and sends it (or pushes it, see below) (`email_agent.py`)

`research_manager.py` orchestrates the four agents. `model_provider.py` is what makes it
all run on OpenRouter: it points the SDK's default OpenAI client at OpenRouter's base URL
and switches it to Chat Completions mode (OpenRouter doesn't support OpenAI's Responses
API or OpenAI's hosted tools, which is also why web search here is a plain Serper API
call rather than OpenAI's built-in `WebSearchTool`).

## Setup

```bash
uv sync
cp .env.example .env   # fill in your API keys
```

Required environment variables (`.env`):

- `OPENROUTER_API_KEY` — every agent's model calls ([openrouter.ai](https://openrouter.ai))
- `SERPER_API_KEY` — web search ([serper.dev](https://serper.dev))
- `DEFAULT_MODEL_NAME` — OpenRouter model slug (default `openai/gpt-4.1-mini`)
- `HOW_MANY_SEARCHES` — how many searches the planner fans out to (default 5)
- `USE_EMAIL` — `true` sends a real email via `EMAIL_*`, `false` sends a Pushover push instead
- `EMAIL_ADDRESS` / `EMAIL_SMTP_SERVER` / `EMAIL_APP_PASSWORD` — required if `USE_EMAIL=true`
- `PUSHOVER_USER` / `PUSHOVER_TOKEN` — required if `USE_EMAIL=false`

## Run

```bash
uv run app.py
```

Opens a Gradio UI. Type a research question, hit Investigate, and watch the status
updates stream in before the full report renders.

## Files

- `app.py` — Gradio UI
- `research_manager.py` — orchestrates the four agents in sequence
- `planner_agent.py`, `search_agent.py`, `writer_agent.py`, `email_agent.py` — the pipeline stages
- `model_provider.py` — configures the OpenRouter client and default model
- `messenger.py` — SMTP email and Pushover push helpers
- `styles.py` — theme, CSS and JS for the UI
