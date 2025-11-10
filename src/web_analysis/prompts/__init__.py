"""Prompts for web analysis workflow."""

from .problem_solution import prompt
from .competition import COMP_PROMPT
from .market_size import MARKET_SIZE_PROMPT

__all__ = ["prompt", "COMP_PROMPT", "MARKET_SIZE_PROMPT"]
