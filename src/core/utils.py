"""Shared utility functions across all modules."""

import os
import re


def slugify(name: str) -> str:
    """Convert a name to a URL-safe slug."""
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", name).strip("-").lower()


def ensure_dir(path: str):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)
