import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

DEFAULT_UA = "Mozilla/5.0 (PitchPanda/1.0; +https://pitchpanda.local)"

def ensure_scheme(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url

def fetch_website_text(url: str, max_chars: int = 10000) -> str:
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

def slugify(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", name).strip("-").lower()

def hostname(url: str) -> str:
    try:
        return urlparse(url).netloc or url
    except:
        return url

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)
