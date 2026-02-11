from pydantic import BaseModel, Field
from typing import List, Optional

class Problem(BaseModel):
    general: str = Field(..., description="1–3 sentence general problem statement")
    example: str = Field(..., description="Concrete, everyday scenario of the problem")

class Solution(BaseModel):
    what_it_is: str = Field(..., description="Short product label, e.g., 'SaaS platform'")
    how_it_works: str = Field(..., description="2–4 sentences on mechanism")
    example: str = Field(..., description="Concrete use case with outcome")

# NEW
class Competitor(BaseModel):
    name: str
    website: Optional[str] = None
    product_type: Optional[str] = None
    sector: Optional[str] = None
    subsector: Optional[str] = None

    # how their PROBLEM overlaps with target (should be near-identical)
    problem_similarity: str = Field(..., description="1–2 lines on how the problem they target matches the startup’s problem")

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

    # NEW
    competition: List[Competitor] = Field(default_factory=list)
