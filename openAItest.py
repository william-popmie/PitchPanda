"""Startup analyzer using LangChain + OpenAI (gpt-5).

This script is intentionally modular. It expects the environment variable
`PITCH_PANDA_API_KEY` or a `.env` file. It uses LangChain's ChatOpenAI with
model_name='gpt-5'.

Install:
  pip install langchain langchain-openai python-dotenv requests beautifulsoup4
"""

import os
import json
from typing import Dict, Any, List, Optional

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

import requests
from bs4 import BeautifulSoup


API_KEY = os.getenv("PITCH_PANDA_API_KEY") or os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("PITCH_PANDA_API_KEY not set. Copy .env.example to .env and set the key, or set OPENAI_API_KEY env var.")

# LangChain uses OPENAI_API_KEY env var; set it for safety
os.environ["OPENAI_API_KEY"] = API_KEY


def fetch_site_snapshot(url: str, timeout: int = 10) -> Dict[str, Optional[str]]:
    try:
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "PitchPandaBot/1.0"})
        r.raise_for_status()
    except Exception as e:
        return {"title": None, "meta": None, "text": None, "error": str(e)}

    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else None
    meta_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    meta = meta_tag.get("content").strip() if meta_tag and meta_tag.get("content") else None

    texts = []
    for tag in ("h1", "h2", "p"):
        for el in soup.find_all(tag, limit=12):
            t = el.get_text(separator=" ", strip=True)
            if t:
                texts.append(t)

    text_snippet = "\n".join(texts[:30])[:4000]
    return {"title": title, "meta": meta, "text": text_snippet, "error": None}


def call_gpt5(prompt: str, temperature: float = 0.0) -> str:
    """Call LangChain ChatOpenAI with gpt-5 and return the assistant text."""
    client = ChatOpenAI(model_name="gpt-5", temperature=temperature)
    system = SystemMessage(content="You are a concise analyst. Provide short factual structured answers.")
    human = HumanMessage(content=prompt)
    resp = client.invoke([system, human])
    # langchain ChatOpenAI returns an AIMessage with .content
    return getattr(resp, "content", str(resp))


def summarize_startup(url: str, snapshot: Dict[str, Optional[str]]) -> Dict[str, Any]:
    prompt = f"""
Given the website URL: {url}

Title: {snapshot.get('title')}
Meta: {snapshot.get('meta')}
Text snippet: {snapshot.get('text')}

Task:
1) Provide a 1-2 sentence "overview" of what the startup does.
2) Provide a 1 sentence "problem" the startup is solving.
3) Provide a 1-2 sentence "solution" describing how they solve it.

Return valid JSON exactly with keys: overview, problem, solution.
Keep each value concise.
"""
    out = call_gpt5(prompt, temperature=0.1)
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out}


def find_founders(url: str, snapshot: Dict[str, Optional[str]]) -> List[Dict[str, Optional[str]]]:
    prompt = f"""
Company website: {url}
Title: {snapshot.get('title')}
Meta: {snapshot.get('meta')}
Text: {snapshot.get('text')}

Task: List the company's founders. For each founder return an object with keys:
  name (string)
  linkedin (string|null)  # a LinkedIn profile URL if known, otherwise null

Return a JSON array of objects.
"""
    out = call_gpt5(prompt, temperature=0.0)
    try:
        data = json.loads(out)
        # Ensure it's a list
        if isinstance(data, list):
            return data
        return [{"raw": out}]
    except Exception:
        return [{"raw": out}]


def find_competitors(url: str, snapshot: Dict[str, Optional[str]]) -> List[Dict[str, str]]:
    prompt = f"""
Company website: {url}
Title: {snapshot.get('title')}
Meta: {snapshot.get('meta')}
Text: {snapshot.get('text')}

Task: Return a JSON array of up to 3 competitor objects with keys:
  name, website, similar, different
Where 'similar' is a 1-sentence note of similarity and 'different' is a 1-sentence note of difference.
"""
    out = call_gpt5(prompt, temperature=0.1)
    try:
        data = json.loads(out)
        if isinstance(data, list):
            return data
        return [{"raw": out}]
    except Exception:
        return [{"raw": out}]


def analyze_startup(url: str) -> Dict[str, Any]:
    snapshot = fetch_site_snapshot(url)
    summary = summarize_startup(url, snapshot)
    founders = find_founders(url, snapshot)
    competitors = find_competitors(url, snapshot)
    return {"url": url, "snapshot": snapshot, "summary": summary, "founders": founders, "competitors": competitors}


if __name__ == "__main__":
    # simple example - replace with any URL
    url = "https://chartera.io"
    result = analyze_startup(url)
    print(json.dumps(result, indent=2, ensure_ascii=False))
