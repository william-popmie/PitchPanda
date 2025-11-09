"""
Render pitch deck analysis to markdown.
"""
from .schemas import DeckAnalysis


def render_deck_markdown(analysis: DeckAnalysis) -> str:
    """
    Render a DeckAnalysis object to markdown format.
    
    Args:
        analysis: The deck analysis to render
    
    Returns:
        Formatted markdown string
    """
    lines = []
    
    # Header
    lines.append(f"# Pitch Deck Analysis: {analysis.deck_name}")
    lines.append(f"\n**Total Slides:** {analysis.total_slides}\n")
    lines.append("---\n")
    
    # Core Elements
    lines.append("## 📊 Core Pitch Elements\n")
    
    if analysis.problem_statement:
        lines.append("### 🔴 Problem Statement")
        lines.append(f"{analysis.problem_statement}\n")
    
    if analysis.solution_overview:
        lines.append("### 💡 Solution Overview")
        lines.append(f"{analysis.solution_overview}\n")
    
    if analysis.value_proposition:
        lines.append("### 🎯 Value Proposition")
        lines.append(f"{analysis.value_proposition}\n")
    
    if analysis.target_market:
        lines.append("### 👥 Target Market")
        lines.append(f"{analysis.target_market}\n")
    
    if analysis.business_model:
        lines.append("### 💰 Business Model")
        lines.append(f"{analysis.business_model}\n")
    
    # Metrics Section (Explicitly Labeled Only)
    if analysis.metrics:
        lines.append("---\n")
        lines.append("## 📈 Explicitly Labeled Metrics\n")
        lines.append("*Note: Only metrics with explicit labels are included as facts.*\n")
        
        # Funding
        if "funding" in analysis.metrics and analysis.metrics["funding"]:
            lines.append("### � Funding")
            for metric in analysis.metrics["funding"]:
                projection_mark = " (Projection)" if metric.is_projection else ""
                context_str = f" - {metric.context}" if metric.context else ""
                lines.append(f"- **{metric.label}**: {metric.value}{projection_mark}{context_str}")
            lines.append("")
        
        # Traction
        if "traction" in analysis.metrics and analysis.metrics["traction"]:
            lines.append("### � Traction")
            for metric in analysis.metrics["traction"]:
                projection_mark = " (Projection)" if metric.is_projection else ""
                context_str = f" - {metric.context}" if metric.context else ""
                lines.append(f"- **{metric.label}**: {metric.value}{projection_mark}{context_str}")
            lines.append("")
        
        # Market Size
        if "market_size" in analysis.metrics and analysis.metrics["market_size"]:
            lines.append("### 🌍 Market Size")
            for metric in analysis.metrics["market_size"]:
                projection_mark = " (Projection)" if metric.is_projection else ""
                context_str = f" - {metric.context}" if metric.context else ""
                lines.append(f"- **{metric.label}**: {metric.value}{projection_mark}{context_str}")
            lines.append("")
        
        # Financials
        if "financials" in analysis.metrics and analysis.metrics["financials"]:
            lines.append("### 💹 Financial Metrics")
            for metric in analysis.metrics["financials"]:
                projection_mark = " (Projection)" if metric.is_projection else ""
                context_str = f" - {metric.context}" if metric.context else ""
                lines.append(f"- **{metric.label}**: {metric.value}{projection_mark}{context_str}")
            lines.append("")
        
        # LOIs
        if "lois" in analysis.metrics and analysis.metrics["lois"]:
            lines.append("### 📝 Letters of Intent (LOIs)")
            for metric in analysis.metrics["lois"]:
                projection_mark = " (Projection)" if metric.is_projection else ""
                context_str = f" - {metric.context}" if metric.context else ""
                lines.append(f"- **{metric.label}**: {metric.value}{projection_mark}{context_str}")
            lines.append("")
        
        # Other metrics
        for category, metrics in analysis.metrics.items():
            if category not in ["funding", "traction", "market_size", "financials", "lois"] and metrics:
                lines.append(f"### 📌 {category.replace('_', ' ').title()}")
                for metric in metrics:
                    projection_mark = " (Projection)" if metric.is_projection else ""
                    context_str = f" - {metric.context}" if metric.context else ""
                    lines.append(f"- **{metric.label}**: {metric.value}{projection_mark}{context_str}")
                lines.append("")
    
    # Team
    if analysis.team:
        lines.append("---\n")
        lines.append("## 👔 Team\n")
        for member in analysis.team:
            name_str = member.name or "Unnamed"
            role_str = f" - **{member.role}**" if member.role else ""
            background_str = f"\n  - {member.background}" if member.background else ""
            lines.append(f"- {name_str}{role_str}{background_str}")
        lines.append("")
    
    # Competition
    if analysis.competition_mentioned:
        lines.append("---\n")
        lines.append("## 🏢 Competition (As Presented)\n")
        lines.append(f"*{analysis.competition_note}*\n")
        for comp in analysis.competition_mentioned:
            lines.append(f"- {comp}")
        lines.append("")
    
    # Observations and Unlabeled Claims
    lines.append("---\n")
    lines.append("## 🔍 Observations & Notes\n")
    
    if analysis.observations:
        lines.append("### Observations")
        for obs in analysis.observations:
            lines.append(f"- {obs}")
        lines.append("")
    
    if analysis.unlabeled_claims:
        lines.append("### ⚠️ Unlabeled or Vague Claims")
        lines.append("*The following claims lack explicit labels or specific metrics:*")
        for claim in analysis.unlabeled_claims:
            lines.append(f"- {claim}")
        lines.append("")
    
    # Data Quality
    if analysis.data_quality_notes:
        lines.append("### 📊 Data Quality Assessment")
        lines.append(f"{analysis.data_quality_notes}\n")
    
    # Present vs Missing Elements
    lines.append("---\n")
    lines.append("## ✅ Deck Completeness\n")
    
    if analysis.present_elements:
        lines.append("### Present Elements")
        for element in analysis.present_elements:
            lines.append(f"- ✅ {element}")
        lines.append("")
    
    if analysis.missing_elements:
        lines.append("### Missing Elements")
        for missing in analysis.missing_elements:
            lines.append(f"- ❌ {missing}")
        lines.append("")
    
    # Slide Details (if available)
    if analysis.slides:
        lines.append("---\n")
        lines.append("## 📑 Slide-by-Slide Breakdown\n")
        
        for slide in analysis.slides:
            lines.append(f"### Slide {slide.slide_number}")
            if slide.slide_title:
                lines.append(f"**Title:** {slide.slide_title}")
            
            if slide.key_points:
                lines.append("**Key Points:**")
                for point in slide.key_points:
                    lines.append(f"- {point}")
            
            if slide.visual_elements:
                lines.append(f"**Visuals:** {slide.visual_elements}")
            
            lines.append("")
    
    return "\n".join(lines)
