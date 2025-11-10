"""
Renderer for merged company analysis.
"""
from typing import List, Optional
from .schemas import (
    MergedAnalysis, 
    SourcedInfo, 
    ConflictingInfo,
    TeamMember,
    Competitor,
    CompetitiveAdvantage
)


def format_source(source: str) -> str:
    """Format source attribution."""
    if source == "pitch deck":
        return "*(pitch deck)*"
    elif source == "web analysis":
        return "*(web analysis)*"
    elif source == "both":
        return "*(pitch deck & web analysis)*"
    return f"*({source})*"


def render_sourced_info(info: Optional[SourcedInfo], prefix: str = "") -> str:
    """Render a SourcedInfo field."""
    if not info or not info.content:
        return f"{prefix}*Information not found*\n"
    return f"{prefix}{info.content} {format_source(info.source)}\n"


def render_conflicting_info(info: Optional[ConflictingInfo], label: str) -> str:
    """Render conflicting information from both sources."""
    if not info:
        return ""
    
    output = f"**{label}:**\n"
    
    if info.pitch_deck_info:
        output += f"- **Pitch Deck**: {info.pitch_deck_info}\n"
    else:
        output += f"- **Pitch Deck**: *Not found*\n"
    
    if info.web_info:
        output += f"- **Web Analysis**: {info.web_info}\n"
    else:
        output += f"- **Web Analysis**: *Not found*\n"
    
    if info.note:
        output += f"- *Note: {info.note}*\n"
    
    return output + "\n"


def render_markdown(analysis: MergedAnalysis) -> str:
    """
    Render the merged analysis to markdown format.
    
    Args:
        analysis: MergedAnalysis object
        
    Returns:
        Markdown formatted string
    """
    lines = []
    
    # Header
    lines.append(f"# {analysis.company_overview.name}")
    lines.append("")
    lines.append("*Comprehensive Company Overview - Merged from Pitch Deck & Web Analysis*")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Company Overview
    lines.append("## 📋 Company Overview")
    lines.append("")
    
    if analysis.company_overview.website:
        lines.append(f"**Website:** {analysis.company_overview.website}")
        lines.append("")
    
    if analysis.company_overview.tagline:
        lines.append("**Tagline:**")
        lines.append(render_sourced_info(analysis.company_overview.tagline, ""))
        lines.append("")
    
    if analysis.company_overview.description:
        lines.append("**Description:**")
        lines.append(render_sourced_info(analysis.company_overview.description, ""))
        lines.append("")
    
    if analysis.company_overview.sector:
        lines.append("**Sector:**")
        lines.append(render_sourced_info(analysis.company_overview.sector, ""))
        lines.append("")
    
    if analysis.company_overview.locations:
        lines.append("**Active Locations:**")
        lines.append(render_sourced_info(analysis.company_overview.locations, ""))
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Problem & Solution
    lines.append("## 🎯 Problem & Solution")
    lines.append("")
    
    if analysis.problem_solution.problem:
        lines.append("### Problem")
        lines.append(render_sourced_info(analysis.problem_solution.problem, ""))
    
    if analysis.problem_solution.solution:
        lines.append("### Solution")
        lines.append(render_sourced_info(analysis.problem_solution.solution, ""))
    
    if analysis.problem_solution.value_proposition:
        lines.append("### Value Proposition")
        lines.append(render_sourced_info(analysis.problem_solution.value_proposition, ""))
    
    if analysis.problem_solution.product_type:
        lines.append("### Product Type")
        lines.append(render_sourced_info(analysis.problem_solution.product_type, ""))
    
    if analysis.problem_solution.how_it_works:
        lines.append("### How It Works")
        lines.append(render_sourced_info(analysis.problem_solution.how_it_works, ""))
    
    lines.append("---")
    lines.append("")
    
    # Market Information
    lines.append("## 📊 Market Information")
    lines.append("")
    
    if analysis.market.target_market:
        lines.append("### Target Market")
        lines.append(render_sourced_info(analysis.market.target_market, ""))
    
    if analysis.market.tam:
        lines.append(render_conflicting_info(analysis.market.tam, "Total Addressable Market (TAM)"))
    
    if analysis.market.sam:
        lines.append("### Serviceable Addressable Market (SAM)")
        lines.append(render_sourced_info(analysis.market.sam, ""))
    
    if analysis.market.som:
        lines.append("### Serviceable Obtainable Market (SOM)")
        lines.append(render_sourced_info(analysis.market.som, ""))
    
    if analysis.market.market_insights:
        lines.append("### Market Insights")
        lines.append("")
        for insight in analysis.market.market_insights:
            lines.append(f"- {insight.content} {format_source(insight.source)}")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Business Model
    lines.append("## 💼 Business Model")
    lines.append("")
    
    if analysis.business_model.overview:
        lines.append("### Overview")
        lines.append(render_sourced_info(analysis.business_model.overview, ""))
    
    if analysis.business_model.revenue_model:
        lines.append("### Revenue Model")
        lines.append(render_sourced_info(analysis.business_model.revenue_model, ""))
    
    if analysis.business_model.pricing:
        lines.append("### Pricing")
        lines.append(render_sourced_info(analysis.business_model.pricing, ""))
    
    if analysis.business_model.customer_acquisition:
        lines.append("### Customer Acquisition")
        lines.append(render_sourced_info(analysis.business_model.customer_acquisition, ""))
    
    if analysis.business_model.partnerships:
        lines.append("### Key Partnerships")
        lines.append(render_sourced_info(analysis.business_model.partnerships, ""))
    
    if analysis.business_model.distribution:
        lines.append("### Distribution Strategy")
        lines.append(render_sourced_info(analysis.business_model.distribution, ""))
    
    lines.append("---")
    lines.append("")
    
    # Team
    if analysis.team:
        lines.append("## 👥 Team")
        lines.append("")
        
        for member in analysis.team:
            lines.append(f"### {member.name}")
            lines.append(f"**Role:** {member.role} {format_source(member.source)}")
            if member.background:
                lines.append(f"**Background:** {member.background}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Financial Data
    lines.append("## 💰 Financial Data & Traction")
    lines.append("")
    
    if analysis.financial_data.funding_raised:
        lines.append("### Funding Raised")
        lines.append("")
        for funding in analysis.financial_data.funding_raised:
            lines.append(f"- {funding.content} {format_source(funding.source)}")
        lines.append("")
    
    if analysis.financial_data.funding_seeking:
        lines.append("### Currently Seeking")
        lines.append(render_sourced_info(analysis.financial_data.funding_seeking, ""))
    
    if analysis.financial_data.revenue:
        lines.append(render_conflicting_info(analysis.financial_data.revenue, "Revenue"))
    
    if analysis.financial_data.traction_metrics:
        lines.append("### Traction & Metrics")
        lines.append("")
        for metric in analysis.financial_data.traction_metrics:
            lines.append(f"- {metric.content} {format_source(metric.source)}")
        lines.append("")
    
    if analysis.financial_data.projections:
        lines.append("### Projections")
        lines.append("")
        for projection in analysis.financial_data.projections:
            lines.append(f"- {projection.content} {format_source(projection.source)}")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Competitive Landscape
    if analysis.competitors:
        lines.append("## 🏆 Competitive Landscape")
        lines.append("")
        
        for competitor in analysis.competitors:
            lines.append(f"### {competitor.name}")
            if competitor.website:
                lines.append(f"**Website:** {competitor.website}")
            if competitor.similarities:
                lines.append(f"**Similarities:** {competitor.similarities}")
            if competitor.differences:
                lines.append(f"**Differences:** {competitor.differences}")
            lines.append(f"{format_source(competitor.source)}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Competitive Advantages
    if analysis.competitive_advantages:
        lines.append("## 🛡️ Competitive Advantages & IP")
        lines.append("")
        
        for advantage in analysis.competitive_advantages:
            lines.append(f"### {advantage.type}")
            lines.append(f"{advantage.description}")
            if advantage.status:
                lines.append(f"**Status:** {advantage.status}")
            lines.append(f"{format_source(advantage.source)}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Technology
    if analysis.technology:
        lines.append("## 🔧 Technology")
        lines.append("")
        lines.append(render_sourced_info(analysis.technology, ""))
        lines.append("---")
        lines.append("")
    
    # Go-to-Market
    if analysis.go_to_market:
        lines.append("## 🚀 Go-to-Market Strategy")
        lines.append("")
        lines.append(render_sourced_info(analysis.go_to_market, ""))
        lines.append("---")
        lines.append("")
    
    # Awards & Recognition
    if analysis.awards_recognition:
        lines.append("## 🏅 Awards & Recognition")
        lines.append("")
        for award in analysis.awards_recognition:
            lines.append(f"- {award.content} {format_source(award.source)}")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Customer Evidence
    if analysis.customer_evidence:
        lines.append("## 💬 Customer Evidence & Validation")
        lines.append("")
        for evidence in analysis.customer_evidence:
            lines.append(f"- {evidence.content} {format_source(evidence.source)}")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Additional Insights
    if analysis.additional_insights:
        lines.append("## 💡 Additional Insights")
        lines.append("")
        for insight in analysis.additional_insights:
            lines.append(f"- {insight.content} {format_source(insight.source)}")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Deck Completeness Notes
    if analysis.deck_completeness_notes:
        lines.append("## 📝 Analysis Notes")
        lines.append("")
        lines.append("### Pitch Deck Completeness")
        lines.append(analysis.deck_completeness_notes)
        lines.append("")
    
    return "\n".join(lines)
