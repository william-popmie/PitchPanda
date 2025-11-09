"""Utility functions for web analysis."""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

DEFAULT_UA = "Mozilla/5.0 (PitchPanda/1.0; +https://pitchpanda.local)"


def ensure_scheme(url: str) -> str:
    """Ensure URL has a scheme (http/https)."""
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


def fetch_website_text(url: str, max_chars: int = 10000) -> str:
    """Fetch and extract text content from a website."""
    url = ensure_scheme(url)
    try:
        resp = requests.get(url, headers={"User-Agent": DEFAULT_UA}, timeout=20)
        resp.raise_for_status()
        html = resp.text
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript", "svg"]):
            tag.decompose()
        text = " ".join(soup.get_text(separator=" ").split())
        text = re.sub(r"\s+", " ", text).strip()
        return text[:max_chars] if text else "(No readable text found on homepage.)"
    except Exception as e:
        return f"(Error fetching site: {e})"


def hostname(url: str) -> str:
    """Extract hostname from URL."""
    try:
        return urlparse(url).netloc or url
    except:
        return url
