"""
Pydantic schemas for merged company analysis.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class SourcedInfo(BaseModel):
    """Information with source attribution."""
    content: str = Field(description="The actual information")
    source: str = Field(description="Source: 'pitch deck', 'web analysis', or 'both'")
    
    
class ConflictingInfo(BaseModel):
    """When deck and web have different information."""
    pitch_deck_info: Optional[str] = Field(default=None, description="Information from pitch deck")
    web_info: Optional[str] = Field(default=None, description="Information from web analysis")
    note: Optional[str] = Field(default=None, description="Note about the conflict")


class CompanyOverview(BaseModel):
    """High-level company information."""
    name: str = Field(description="Company name")
    website: Optional[str] = Field(default=None, description="Company website")
    tagline: Optional[SourcedInfo] = Field(default=None, description="Company tagline or one-liner")
    description: Optional[SourcedInfo] = Field(default=None, description="Company description")
    sector: Optional[SourcedInfo] = Field(default=None, description="Industry sector")
    locations: Optional[SourcedInfo] = Field(default=None, description="Active locations")


class ProblemSolution(BaseModel):
    """Problem and solution information."""
    problem_web: Optional[str] = Field(default=None, description="Problem statement from web (general)")
    problem_example_web: Optional[str] = Field(default=None, description="Problem example from web")
    problem_deck: Optional[str] = Field(default=None, description="Additional problem details from pitch deck")
    
    solution_web: Optional[str] = Field(default=None, description="Solution from web (product name, how it works)")
    solution_example_web: Optional[str] = Field(default=None, description="Solution example from web")
    solution_deck: Optional[str] = Field(default=None, description="Additional solution details from pitch deck")
    
    value_proposition: Optional[SourcedInfo] = Field(default=None, description="Value proposition")
    product_type: Optional[SourcedInfo] = Field(default=None, description="Type of product/service")
    how_it_works: Optional[SourcedInfo] = Field(default=None, description="How the solution works")


class MarketInfo(BaseModel):
    """Market size and opportunity."""
    target_market: Optional[SourcedInfo] = Field(default=None, description="Target market description")
    tam: Optional[ConflictingInfo] = Field(default=None, description="Total Addressable Market")
    sam: Optional[SourcedInfo] = Field(default=None, description="Serviceable Addressable Market")
    som: Optional[SourcedInfo] = Field(default=None, description="Serviceable Obtainable Market")
    market_insights: List[SourcedInfo] = Field(default_factory=list, description="Additional market insights")


class BusinessModel(BaseModel):
    """Business model and revenue information."""
    overview: Optional[SourcedInfo] = Field(default=None, description="Business model overview")
    revenue_model: Optional[SourcedInfo] = Field(default=None, description="How the company makes money")
    pricing: Optional[SourcedInfo] = Field(default=None, description="Pricing strategy")
    customer_acquisition: Optional[SourcedInfo] = Field(default=None, description="Customer acquisition strategy")
    partnerships: Optional[SourcedInfo] = Field(default=None, description="Key partnerships")
    distribution: Optional[SourcedInfo] = Field(default=None, description="Distribution strategy")


class TeamMember(BaseModel):
    """Individual team member."""
    name: str = Field(description="Team member name")
    role: str = Field(description="Role or title")
    background: Optional[str] = Field(default=None, description="Background or experience")
    source: str = Field(description="Source: 'pitch deck', 'web analysis', or 'both'")


class FinancialData(BaseModel):
    """Financial metrics and funding."""
    funding_raised: List[SourcedInfo] = Field(default_factory=list, description="Funding raised to date")
    funding_seeking: Optional[SourcedInfo] = Field(default=None, description="Currently seeking funding")
    revenue: Optional[ConflictingInfo] = Field(default=None, description="Revenue figures")
    traction_metrics: List[SourcedInfo] = Field(default_factory=list, description="Traction and metrics")
    projections: List[SourcedInfo] = Field(default_factory=list, description="Financial projections")


class Competitor(BaseModel):
    """Competitor information."""
    name: str = Field(description="Competitor name")
    website: Optional[str] = Field(default=None, description="Competitor website")
    similarities: Optional[str] = Field(default=None, description="How they're similar")
    differences: Optional[str] = Field(default=None, description="How they differ")
    source: str = Field(description="Source: 'pitch deck', 'web analysis', or 'both'")


class CompetitiveAdvantage(BaseModel):
    """Competitive advantage or IP."""
    type: str = Field(description="Type: patent, network effects, proprietary tech, etc.")
    description: str = Field(description="Description of the advantage")
    status: Optional[str] = Field(default=None, description="Status: granted, pending, etc.")
    source: str = Field(description="Source: 'pitch deck', 'web analysis', or 'both'")


class MergedAnalysis(BaseModel):
    """Complete merged company analysis."""
    company_overview: CompanyOverview = Field(description="Company overview")
    problem_solution: ProblemSolution = Field(description="Problem and solution")
    market: MarketInfo = Field(description="Market information")
    business_model: BusinessModel = Field(description="Business model")
    team: List[TeamMember] = Field(default_factory=list, description="Team members")
    financial_data: FinancialData = Field(description="Financial data and metrics")
    competitors: List[Competitor] = Field(default_factory=list, description="Competitors")
    competitive_advantages: List[CompetitiveAdvantage] = Field(default_factory=list, description="Competitive advantages")
    technology: Optional[SourcedInfo] = Field(default=None, description="Technology details")
    go_to_market: Optional[SourcedInfo] = Field(default=None, description="Go-to-market strategy")
    awards_recognition: List[SourcedInfo] = Field(default_factory=list, description="Awards and recognition")
    customer_evidence: List[SourcedInfo] = Field(default_factory=list, description="Customer testimonials and evidence")
    additional_insights: List[SourcedInfo] = Field(default_factory=list, description="Any other relevant information")
    deck_completeness_notes: Optional[str] = Field(default=None, description="Notes about deck completeness (from pitch deck analysis)")
