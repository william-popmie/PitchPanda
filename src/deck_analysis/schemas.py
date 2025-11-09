"""
Pydantic schemas for pitch deck analysis.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Metric(BaseModel):
    """A single metric extracted from the deck - captures ALL numbers."""
    label: str  # e.g., "MRR", "Seed Funding", "ARR", "TAM", or inferred like "Funding (uncertain)"
    value: str  # The actual value as shown (e.g., "$50K", "500 users", "$2M")
    context: Optional[str] = None  # Additional context if needed
    is_projection: bool = False  # True if this is a future projection
    confidence: str = "high"  # "high" (explicitly labeled), "medium" (inferred), "low" (vague/uncertain)
    notes: Optional[str] = None  # e.g., "Seems unrealistic", "Label unclear", "Inferred from context"


class TeamMember(BaseModel):
    """Information about a team member."""
    name: Optional[str] = None
    role: Optional[str] = None  # CEO, CTO, COO, etc.
    background: Optional[str] = None  # Previous experience, ex-founder at X, etc.


class SlideInsight(BaseModel):
    """Analysis of a single slide."""
    slide_number: int
    slide_title: Optional[str] = None
    key_points: List[str] = Field(default_factory=list)
    visual_elements: Optional[str] = None  # Description of charts, images, etc.
    

class DeckAnalysis(BaseModel):
    """Complete pitch deck analysis - factual and unbiased."""
    deck_name: str
    total_slides: int
    
    # Core pitch elements (descriptive, not persuasive)
    problem_statement: Optional[str] = None
    solution_overview: Optional[str] = None
    value_proposition: Optional[str] = None
    target_market: Optional[str] = None
    business_model: Optional[str] = None
    
    # Explicitly labeled metrics ONLY
    metrics: Dict[str, List[Metric]] = Field(default_factory=dict)
    # Organized by category: "funding", "traction", "market_size", "financials", "lois", etc.
    
    # Team information
    team: List[TeamMember] = Field(default_factory=list)
    
    # Competition (as presented - note bias)
    competition_mentioned: List[str] = Field(default_factory=list)
    competition_note: Optional[str] = "Competition as presented in deck may be biased"
    
    # Notes and observations (not facts)
    observations: List[str] = Field(default_factory=list)
    unlabeled_claims: List[str] = Field(default_factory=list)  # Vague claims without explicit labels
    
    # Slide-by-slide insights
    slides: List[SlideInsight] = Field(default_factory=list)
    
    # Factual assessment
    present_elements: List[str] = Field(default_factory=list)  # What IS in the deck
    missing_elements: List[str] = Field(default_factory=list)  # Standard elements NOT in deck
    data_quality_notes: Optional[str] = None  # Notes on explicit vs vague labeling
