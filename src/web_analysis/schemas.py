"""Schemas for web analysis workflow."""

from pydantic import BaseModel, Field
from typing import List, Optional


class MarketSize(BaseModel):
    tam: str = Field(..., description="Total Addressable Market with numerical estimate and context")
    sam: str = Field(..., description="Serviceable Addressable Market with numerical estimate and context")
    som: str = Field(..., description="Serviceable Obtainable Market with numerical estimate and context")
    calculation_context: str = Field(..., description="Explanation of how these numbers were calculated, assumptions made, and caveats")
    note: str = Field(default="These are rough estimates based on available data and should be validated with primary research.")


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

    # evidence
    sources: List[str] = Field(default_factory=list)


class Analysis(BaseModel):
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
