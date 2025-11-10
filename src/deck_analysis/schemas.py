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


class UnconventionalData(BaseModel):
    """Captures any unconventional, unusual, or hard-to-categorize information from the deck."""
    category: str  # e.g., "customer_quote", "case_study", "technical_detail", "market_insight", "unusual_metric", etc.
    content: str  # The actual information
    source: str  # Where in deck (e.g., "Slide 7", "Appendix")
    trustworthiness: str  # "explicit" (clearly stated), "inferred" (reasonable interpretation), "vague" (unclear/ambiguous), "unverifiable" (claim without evidence)
    context: Optional[str] = None  # Additional context to help reader understand
    notes: Optional[str] = None  # Any flags, concerns, or clarifications (e.g., "seems inflated", "no supporting data")


class AdditionalInsight(BaseModel):
    """Captures additional interesting information that doesn't fit standard categories."""
    title: str  # Brief title for this insight
    description: str  # The actual information
    source: str  # Where found (slide number, section)
    confidence: str  # "high", "medium", "low"
    relevance: Optional[str] = None  # Why this matters or what it indicates
    flags: List[str] = Field(default_factory=list)  # Any concerns or notes


class TextHeavySection(BaseModel):
    """For slides with lots of text or detailed explanations that don't fit other categories."""
    title: str  # Section or slide title
    content: str  # Full text content or key excerpts
    slide_numbers: List[int] = Field(default_factory=list)  # Where this appears
    data_type: str  # "explanation", "description", "methodology", "case_study", "testimonial", etc.
    key_takeaways: List[str] = Field(default_factory=list)  # Main points
    trustworthiness: str  # How reliable is this information
    notes: Optional[str] = None


class SlideInsight(BaseModel):
    """Analysis of a single slide."""
    slide_number: int
    slide_title: Optional[str] = None
    key_points: List[str] = Field(default_factory=list)
    visual_elements: Optional[str] = None  # Description of charts, images, etc.
    additional_content: Optional[str] = None  # Any other interesting content on this slide
    data_items: List[str] = Field(default_factory=list)  # Specific data points or numbers mentioned
    

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
    
    # UNCONVENTIONAL & ADDITIONAL DATA (capture everything interesting)
    unconventional_data: List[UnconventionalData] = Field(default_factory=list)  # Unusual or hard-to-categorize info
    additional_insights: List[AdditionalInsight] = Field(default_factory=list)  # Extra interesting findings
    text_heavy_sections: List[TextHeavySection] = Field(default_factory=list)  # Detailed text content
    
    # Customer evidence & validation
    customer_testimonials: List[str] = Field(default_factory=list)  # Direct quotes or testimonials
    case_studies: List[str] = Field(default_factory=list)  # Detailed customer case studies
    pilot_programs: List[str] = Field(default_factory=list)  # Pilot or trial program results
    
    # Market & industry insights from deck
    market_insights: List[str] = Field(default_factory=list)  # Market trends, data points mentioned
    industry_statistics: List[str] = Field(default_factory=list)  # Third-party stats cited
    
    # Go-to-market & strategy details
    gtm_strategy_details: Optional[str] = None  # Detailed go-to-market approach
    marketing_channels: List[str] = Field(default_factory=list)  # Specific channels mentioned
    sales_strategy: Optional[str] = None  # Sales approach details
    
    # Technology & product details
    technology_stack: List[str] = Field(default_factory=list)  # Technologies mentioned
    technical_approach: Optional[str] = None  # How the product works technically
    product_roadmap: List[str] = Field(default_factory=list)  # Future product plans
    integration_partners: List[str] = Field(default_factory=list)  # Technical integrations
    
    # Risk & challenges (if mentioned)
    risks_acknowledged: List[str] = Field(default_factory=list)  # Risks the company acknowledges
    mitigation_strategies: List[str] = Field(default_factory=list)  # How they plan to address risks
    
    # Media & press mentions
    press_coverage: List[str] = Field(default_factory=list)  # Media mentions, press coverage
    thought_leadership: List[str] = Field(default_factory=list)  # Speaking engagements, publications
    
    # Factual assessment
    present_elements: List[str] = Field(default_factory=list)  # What IS in the deck
    missing_elements: List[str] = Field(default_factory=list)  # Standard elements NOT in deck
    data_quality_notes: Optional[str] = None  # Notes on explicit vs vague labeling
    
    # Overall assessment notes
    deck_quality_assessment: Optional[str] = None  # Overall impression of deck quality, completeness
    notable_strengths: List[str] = Field(default_factory=list)  # What the deck does well
    notable_weaknesses: List[str] = Field(default_factory=list)  # What's missing or unclear
