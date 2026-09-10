import os

import requests
from agents import Agent, ModelSettings, function_tool

from model_provider import MODEL

INSTRUCTIONS = """
You are a research assistant. Given a search term, you search the web for that term and
produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 words.
Capture the main points and be succinct. Reply only with the summary.
"""


@function_tool
def web_search(query: str) -> str:
    """Search the web for the given query and return the top results."""
    response = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": os.getenv("SERPER_API_KEY"), "Content-Type": "application/json"},
        json={"q": query},
    )
    response.raise_for_status()
    results = response.json().get("organic", [])
    if not results:
        return "No results found."
    return "\n\n".join(
        f"{r.get('title', '')}\n{r.get('link', '')}\n{r.get('snippet', '')}" for r in results[:8]
    )


settings = ModelSettings(tool_choice="required")
tools = [web_search]

search_agent = Agent(name="Search Agent", instructions=INSTRUCTIONS, tools=tools, model=MODEL, model_settings=settings)
