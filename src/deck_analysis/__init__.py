"""
Pitch deck analysis module for PitchPanda.

Converts PDF pitch decks to images and analyzes them with GPT-4 Vision
to extract insights about market, team, product, metrics, and more.
"""

from .graph import deck_graph, DeckState
from .schemas import DeckAnalysis, SlideInsight
from .main import analyze_deck

__all__ = [
    "deck_graph",
    "DeckState",
    "DeckAnalysis",
    "SlideInsight",
    "analyze_deck",
]

