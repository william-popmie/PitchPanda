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
    """Complete evaluation with scores and analysis - VC CRITICAL PERSPECTIVE."""
    company_name: str = Field(description="Name of the company")
    
    # Scoring criteria (1-5 scale) - VC perspective with high bar
    team: Criterion = Field(description="Team score: 1=solo/weak team, 3=competent, 5=exceptional with exits")
    technology: Criterion = Field(description="Technology score: 1=idea only, 3=working product, 5=market-leading with strong IP")
    market: Criterion = Field(description="Market score (CRITICAL): 1=<$1B TAM, 3=$5-20B TAM, 5=>$50B TAM with growth")
    value_proposition: Criterion = Field(description="Value proposition: 1=vitamin, 3=good painkiller, 5=10x better solution")
    competitive_advantage: Criterion = Field(description="MOAT score: 1=no moat, 3=some moat, 5=multiple compounding moats")
    social_impact: Criterion = Field(description="Social impact: 1=none, 3=moderate impact, 5=transformative")
    
    # Overall score (average of all criteria)
    overall_score: float = Field(description="Average score across all criteria")
    
    # Competitor analysis
    competitor_groups: List[CompetitorGroup] = Field(
        default_factory=list,
        description="Competitors grouped by similar characteristics"
    )
    
    # Final comments - be brutally honest about investment potential
    comments: str = Field(description="CRITICAL remarks: revenue metrics, red flags, VC fit, deal concerns, unicorn potential")
