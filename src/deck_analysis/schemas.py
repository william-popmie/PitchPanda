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


class CompetitiveAdvantage(BaseModel):
    """Competitive advantages, IP, patents, etc."""
    category: str  # "patent_secured", "patent_pending", "trade_secret", "exclusive_partnership", "proprietary_technology", "regulatory_approval", etc.
    description: str
    status: Optional[str] = None  # "granted", "pending", "filed", "in_process", etc.
    details: Optional[str] = None  # Patent numbers, filing dates, specific details
    confidence: str = "high"  # How clearly this is stated in the deck


class AwardOrGrant(BaseModel):
    """Awards, grants, or recognition received."""
    type: str  # "grant", "award", "competition_win", "accelerator", "government_program", etc.
    name: str  # Name of the award/grant
    amount: Optional[str] = None  # Dollar amount if applicable
    year: Optional[str] = None  # When received
    organization: Optional[str] = None  # Who gave it
    is_non_dilutive: Optional[bool] = None  # For funding: is it non-dilutive?


class FundingDetail(BaseModel):
    """Detailed funding information."""
    type: str  # "pre_seed", "seed", "series_a", "series_b", "grant", "non_dilutive", "convertible_note", "safe", etc.
    amount: str
    date: Optional[str] = None
    investors: List[str] = Field(default_factory=list)
    is_non_dilutive: bool = False
    valuation: Optional[str] = None  # Pre-money or post-money if mentioned
    notes: Optional[str] = None


class BusinessModelDetail(BaseModel):
    """Detailed business model information beyond just 'how they make money'."""
    revenue_model: Optional[str] = None  # Subscription, transaction fee, licensing, etc.
    pricing_structure: Optional[str] = None  # Specific pricing if mentioned
    customer_acquisition: Optional[str] = None  # How they acquire customers
    sales_cycle: Optional[str] = None  # Length and process
    partnerships: List[str] = Field(default_factory=list)  # Key partnerships mentioned
    distribution_channels: List[str] = Field(default_factory=list)
    expansion_strategy: Optional[str] = None  # Geographic or market expansion plans
    notes: List[str] = Field(default_factory=list)  # Additional observations


class ProjectionAnalysis(BaseModel):
    """Critical analysis of projections vs facts."""
    metric_name: str  # What's being projected
    current_value: Optional[str] = None  # Current state
    projected_value: str  # Future projection
    timeframe: Optional[str] = None  # When the projection is for
    assumptions_stated: List[str] = Field(default_factory=list)  # What assumptions are mentioned
    realism_assessment: Optional[str] = None  # Critical assessment of whether this seems realistic
    supporting_evidence: List[str] = Field(default_factory=list)  # What evidence supports this
    flags: List[str] = Field(default_factory=list)  # Red flags or concerns


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
    business_model: Optional[str] = None  # High-level overview
    
    # Detailed business model analysis
    business_model_details: Optional[BusinessModelDetail] = None
    
    # Explicitly labeled metrics ONLY
    metrics: Dict[str, List[Metric]] = Field(default_factory=dict)
    # Organized by category: "funding", "traction", "market_size", "financials", "lois", etc.
    
    # Detailed funding breakdown
    funding_details: List[FundingDetail] = Field(default_factory=list)
    
    # Team information
    team: List[TeamMember] = Field(default_factory=list)
    
    # Competitive advantages (IP, patents, etc.)
    competitive_advantages: List[CompetitiveAdvantage] = Field(default_factory=list)
    
    # Awards, grants, recognition
    awards_and_grants: List[AwardOrGrant] = Field(default_factory=list)
    
    # Competition (as presented - note bias)
    competition_mentioned: List[str] = Field(default_factory=list)
    competition_note: Optional[str] = "Competition as presented in deck may be biased"
    
    # Critical analysis of projections
    projection_analysis: List[ProjectionAnalysis] = Field(default_factory=list)
    
    # Distinguish between facts and storytelling
    facts: List[str] = Field(default_factory=list)  # Verifiable facts with evidence
    storytelling: List[str] = Field(default_factory=list)  # Claims, narratives, aspirations without hard evidence
    
    # Notes and observations (not facts)
    observations: List[str] = Field(default_factory=list)
    unlabeled_claims: List[str] = Field(default_factory=list)  # Vague claims without explicit labels
    
    # Slide-by-slide insights
    slides: List[SlideInsight] = Field(default_factory=list)
    
    # Factual assessment
    present_elements: List[str] = Field(default_factory=list)  # What IS in the deck
    missing_elements: List[str] = Field(default_factory=list)  # Standard elements NOT in deck
    data_quality_notes: Optional[str] = None  # Notes on explicit vs vague labeling
