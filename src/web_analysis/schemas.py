"""Schemas for web analysis workflow."""

from pydantic import BaseModel, Field
from typing import List, Optional


class MarketSizeEstimate(BaseModel):
    """Structured market size calculation with explicit formula."""
    value: str = Field(..., description="Market size value (e.g., '$4.2B', '$840M')")
    formula: str = Field(..., description="Explicit calculation showing variables and math")
    assumptions: List[str] = Field(default_factory=list, description="Key assumptions made in the calculation")
    unit: str = Field(..., description="Unit of measurement (e.g., 'companies', 'users', 'transactions')")


class MarketSize(BaseModel):
    tam: MarketSizeEstimate = Field(..., description="Total Addressable Market with formula-based calculation")
    sam: MarketSizeEstimate = Field(..., description="Serviceable Addressable Market with formula-based calculation")
    som: MarketSizeEstimate = Field(..., description="Serviceable Obtainable Market with formula-based calculation")
    calculation_note: str = Field(..., description="Confidence level, data quality assessment, and key risks")


class Problem(BaseModel):
    general: str = Field(..., description="1–3 sentence general problem statement")
    example: str = Field(..., description="Concrete, everyday scenario of the problem")


class Solution(BaseModel):
    what_it_is: str = Field(..., description="Short product label, e.g., 'SaaS platform'")
    how_it_works: str = Field(..., description="2–4 sentences on mechanism")
    example: str = Field(..., description="Concrete use case with outcome")


class Competitor(BaseModel):
    name: str
    website: Optional[str] = None
    product_type: Optional[str] = None
    sector: Optional[str] = None
    subsector: Optional[str] = None

    # how their PROBLEM overlaps with target (should be near-identical)
    problem_similarity: str = Field(..., description="1–2 lines on how the problem they target matches the startup's problem")

    # solution + contrast
    solution_summary: str = Field(..., description="What they do / how it works (2–4 lines)")
    similarities: List[str] = Field(default_factory=list, description="Bullets of overlap (approach, audience, data sources, GTM, etc.)")
    differences: List[str] = Field(default_factory=list, description="Bullets of differences (business model, tech, segment, pricing, integrations, etc.)")

    # where they're active
    active_locations: List[str] = Field(default_factory=list)

    # evidence and quality
    sources: List[str] = Field(default_factory=list, description="URLs used as evidence for this competitor")
    confidence: Optional[str] = Field(default="medium", description="high | medium | low - confidence in the match")
    why_included: Optional[str] = Field(default="", description="One-line justification linking target's problem to this competitor")


class Analysis(BaseModel):
    company_summary: str = Field(..., description="2-3 sentence elevator pitch describing the company")
    problem: Problem
    solution: Solution
    product_type: str
    sector: str
    subsector: str
    active_locations: List[str] = Field(default_factory=list)
    sources: List[str]

    # Market size data
    market_size: Optional[MarketSize] = None

    # Competition data
    competition: List[Competitor] = Field(default_factory=list)
