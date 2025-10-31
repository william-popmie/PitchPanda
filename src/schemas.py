from pydantic import BaseModel, Field
from typing import List

class Problem(BaseModel):
    general: str = Field(..., description="1–3 sentence general problem statement")
    example: str = Field(..., description="Concrete, everyday scenario of the problem")

class Solution(BaseModel):
    what_it_is: str = Field(..., description="Short product label, e.g., 'SaaS platform'")
    how_it_works: str = Field(..., description="2–4 sentences on mechanism")
    example: str = Field(..., description="Concrete use case with outcome")

class Analysis(BaseModel):
    problem: Problem
    solution: Solution
    product_type: str
    sector: str
    subsector: str
    sources: List[str]
