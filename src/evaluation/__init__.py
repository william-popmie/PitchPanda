"""
Pydantic schemas for company evaluation (scoring).
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class Criterion(BaseModel):
    """Individual scoring criterion."""
    name: str = Field(description="Name of the criterion")
    score: int = Field(ge=1, le=5, description="Score from 1-5")
    reasoning: str = Field(description="Brief explanation of the score")


class CompetitorGroup(BaseModel):
    """Group of similar competitors."""
    group_name: str = Field(description="Name for this group of competitors")
    competitors: List[str] = Field(description="List of competitor names in this group")
    characteristics: str = Field(description="What makes this group similar")


class CompanyEvaluation(BaseModel):
    """Complete evaluation with scores and analysis."""
    company_name: str = Field(description="Name of the company")
    
    # Scoring criteria (1-5 scale)
    team: Criterion = Field(description="Team score: 1=lone founder, 5=experienced team")
    technology: Criterion = Field(description="Technology score: 1=idea stage, 5=market ready")
    market: Criterion = Field(description="Market score: 1=small, 5=very large")
    value_proposition: Criterion = Field(description="Value proposition score: 1=doesn't solve, 5=perfect fit")
    competitive_advantage: Criterion = Field(description="MOAT score: 1=no MOAT, 5=very strong MOAT")
    social_impact: Criterion = Field(description="Social impact score: 1=no impact, 5=transformative")
    
    # Overall score (average of all criteria)
    overall_score: float = Field(description="Average score across all criteria")
    
    # Competitor analysis
    competitor_groups: List[CompetitorGroup] = Field(
        default_factory=list,
        description="Competitors grouped by similar characteristics"
    )
    
    # Final comments
    comments: str = Field(description="Final remarks, interesting observations, or concerns")
