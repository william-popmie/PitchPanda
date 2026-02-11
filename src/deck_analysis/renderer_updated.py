"""
Render pitch deck analysis to markdown with confidence levels.
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
    
    # Detailed Business Model
    if analysis.business_model_details:
        lines.append("### 💼 Business Model Details")
        bm = analysis.business_model_details
        if bm.revenue_model:
            lines.append(f"**Revenue Model:** {bm.revenue_model}")
        if bm.pricing_structure:
            lines.append(f"**Pricing:** {bm.pricing_structure}")
        if bm.customer_acquisition:
            lines.append(f"**Customer Acquisition:** {bm.customer_acquisition}")
        if bm.sales_cycle:
            lines.append(f"**Sales Cycle:** {bm.sales_cycle}")
        if bm.partnerships:
            lines.append(f"**Partnerships:** {', '.join(bm.partnerships)}")
        if bm.distribution_channels:
            lines.append(f"**Distribution:** {', '.join(bm.distribution_channels)}")
        if bm.expansion_strategy:
            lines.append(f"**Expansion Strategy:** {bm.expansion_strategy}")
        if bm.notes:
            lines.append("**Additional Notes:**")
            for note in bm.notes:
                lines.append(f"- {note}")
        lines.append("")
    
    # Metrics Section (ALL numbers with confidence levels)
    if analysis.metrics:
        lines.append("---\n")
        lines.append("## 📈 Metrics & Numbers\n")
        
        # Funding
        if "funding" in analysis.metrics and analysis.metrics["funding"]:
            lines.append("### 💵 Funding")
            for metric in analysis.metrics["funding"]:
                # Build context string
                parts = []
                if metric.is_projection:
                    parts.append("*Projection*")
                if metric.context:
                    parts.append(metric.context)
                if metric.confidence in ["medium", "low"]:
                    parts.append(f"inferred from context" if metric.confidence == "medium" else "uncertain")
                
                ctx = f" ({' - '.join(parts)})" if parts else ""
                note = f"\n  > *Note: {metric.notes}*" if metric.notes else ""
                lines.append(f"- **{metric.label}**: {metric.value}{ctx}{note}")
            lines.append("")
        
        # Traction
        if "traction" in analysis.metrics and analysis.metrics["traction"]:
            lines.append("### 📊 Traction")
            for metric in analysis.metrics["traction"]:
                parts = []
                if metric.is_projection:
                    parts.append("*Projection*")
                if metric.context:
                    parts.append(metric.context)
                if metric.confidence in ["medium", "low"]:
                    parts.append(f"inferred from context" if metric.confidence == "medium" else "uncertain")
                
                ctx = f" ({' - '.join(parts)})" if parts else ""
                note = f"\n  > *Note: {metric.notes}*" if metric.notes else ""
                lines.append(f"- **{metric.label}**: {metric.value}{ctx}{note}")
            lines.append("")
        
        # Market Size
        if "market_size" in analysis.metrics and analysis.metrics["market_size"]:
            lines.append("### 🌍 Market Size")
            for metric in analysis.metrics["market_size"]:
                parts = []
                if metric.is_projection:
                    parts.append("*Projection*")
                if metric.context:
                    parts.append(metric.context)
                if metric.confidence in ["medium", "low"]:
                    parts.append(f"inferred from context" if metric.confidence == "medium" else "uncertain")
                
                ctx = f" ({' - '.join(parts)})" if parts else ""
                note = f"\n  > *Note: {metric.notes}*" if metric.notes else ""
                lines.append(f"- **{metric.label}**: {metric.value}{ctx}{note}")
            lines.append("")
        
        # Financials
        if "financials" in analysis.metrics and analysis.metrics["financials"]:
            lines.append("### 💹 Financial Metrics")
            for metric in analysis.metrics["financials"]:
                parts = []
                if metric.is_projection:
                    parts.append("*Projection*")
                if metric.context:
                    parts.append(metric.context)
                if metric.confidence in ["medium", "low"]:
                    parts.append(f"inferred from context" if metric.confidence == "medium" else "uncertain")
                
                ctx = f" ({' - '.join(parts)})" if parts else ""
                note = f"\n  > *Note: {metric.notes}*" if metric.notes else ""
                lines.append(f"- **{metric.label}**: {metric.value}{ctx}{note}")
            lines.append("")
        
        # LOIs
        if "lois" in analysis.metrics and analysis.metrics["lois"]:
            lines.append("### 📝 Letters of Intent (LOIs)")
            for metric in analysis.metrics["lois"]:
                parts = []
                if metric.is_projection:
                    parts.append("*Projection*")
                if metric.context:
                    parts.append(metric.context)
                if metric.confidence in ["medium", "low"]:
                    parts.append(f"inferred from context" if metric.confidence == "medium" else "uncertain")
                
                ctx = f" ({' - '.join(parts)})" if parts else ""
                note = f"\n  > *Note: {metric.notes}*" if metric.notes else ""
                lines.append(f"- **{metric.label}**: {metric.value}{ctx}{note}")
            lines.append("")
        
        # Other metrics
        for category, metrics in analysis.metrics.items():
            if category not in ["funding", "traction", "market_size", "financials", "lois"] and metrics:
                lines.append(f"### 📌 {category.replace('_', ' ').title()}")
                for metric in metrics:
                    parts = []
                    if metric.is_projection:
                        parts.append("*Projection*")
                    if metric.context:
                        parts.append(metric.context)
                    if metric.confidence in ["medium", "low"]:
                        parts.append(f"inferred from context" if metric.confidence == "medium" else "uncertain")
                    
                    ctx = f" ({' - '.join(parts)})" if parts else ""
                    note = f"\n  > *Note: {metric.notes}*" if metric.notes else ""
                    lines.append(f"- **{metric.label}**: {metric.value}{ctx}{note}")
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
    
    # Competitive Advantages (IP, Patents, etc.)
    if analysis.competitive_advantages:
        lines.append("---\n")
        lines.append("## 🛡️ Competitive Advantages & IP\n")
        
        # Group by category
        categories = {}
        for adv in analysis.competitive_advantages:
            cat = adv.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(adv)
        
        for cat, advs in categories.items():
            cat_display = cat.replace('_', ' ').title()
            lines.append(f"### {cat_display}")
            for adv in advs:
                status_str = f" (*{adv.status}*)" if adv.status else ""
                conf_str = "" if adv.confidence == "high" else f" - *confidence: {adv.confidence}*"
                lines.append(f"- **{adv.description}**{status_str}{conf_str}")
                if adv.details:
                    lines.append(f"  - Details: {adv.details}")
            lines.append("")
    
    # Awards and Grants
    if analysis.awards_and_grants:
        lines.append("---\n")
        lines.append("## 🏆 Awards, Grants & Recognition\n")
        
        # Separate dilutive and non-dilutive funding
        non_dilutive = [a for a in analysis.awards_and_grants if a.is_non_dilutive]
        other_awards = [a for a in analysis.awards_and_grants if not a.is_non_dilutive or a.is_non_dilutive is None]
        
        if non_dilutive:
            lines.append("### 💰 Non-Dilutive Funding")
            for award in non_dilutive:
                amount_str = f" - **{award.amount}**" if award.amount else ""
                year_str = f" ({award.year})" if award.year else ""
                org_str = f"\n  - From: {award.organization}" if award.organization else ""
                lines.append(f"- **{award.name}**{amount_str}{year_str}{org_str}")
            lines.append("")
        
        if other_awards:
            lines.append("### 🎖️ Awards & Recognition")
            for award in other_awards:
                amount_str = f" - **{award.amount}**" if award.amount else ""
                year_str = f" ({award.year})" if award.year else ""
                org_str = f"\n  - From: {award.organization}" if award.organization else ""
                lines.append(f"- **{award.name}**{amount_str}{year_str}{org_str}")
            lines.append("")
    
    # Detailed Funding Breakdown
    if analysis.funding_details:
        lines.append("---\n")
        lines.append("## 💵 Detailed Funding Breakdown\n")
        
        # Separate by type
        equity = [f for f in analysis.funding_details if not f.is_non_dilutive]
        non_dilutive = [f for f in analysis.funding_details if f.is_non_dilutive]
        
        if equity:
            lines.append("### Equity Funding")
            for fund in equity:
                date_str = f" ({fund.date})" if fund.date else ""
                lines.append(f"- **{fund.type.replace('_', ' ').title()}**: {fund.amount}{date_str}")
                if fund.investors:
                    lines.append(f"  - Investors: {', '.join(fund.investors)}")
                if fund.valuation:
                    lines.append(f"  - Valuation: {fund.valuation}")
                if fund.notes:
                    lines.append(f"  - Notes: {fund.notes}")
            lines.append("")
        
        if non_dilutive:
            lines.append("### Non-Dilutive Funding")
            for fund in non_dilutive:
                date_str = f" ({fund.date})" if fund.date else ""
                lines.append(f"- **{fund.type.replace('_', ' ').title()}**: {fund.amount}{date_str}")
                if fund.investors:
                    lines.append(f"  - Source: {', '.join(fund.investors)}")
                if fund.notes:
                    lines.append(f"  - Notes: {fund.notes}")
            lines.append("")
    
    # Competition
    if analysis.competition_mentioned:
        lines.append("---\n")
        lines.append("## 🏢 Competition (As Presented)\n")
        lines.append(f"*{analysis.competition_note}*\n")
        for comp in analysis.competition_mentioned:
            lines.append(f"- {comp}")
        lines.append("")
    
    # Projection Analysis
    if analysis.projection_analysis:
        lines.append("---\n")
        lines.append("## 📊 Projection Analysis (Critical Assessment)\n")
        lines.append("*Critical analysis of projections vs. current state and supporting evidence.*\n")
        
        for proj in analysis.projection_analysis:
            lines.append(f"### {proj.metric_name}")
            if proj.current_value:
                lines.append(f"**Current:** {proj.current_value}")
            lines.append(f"**Projected:** {proj.projected_value}")
            if proj.timeframe:
                lines.append(f"**Timeframe:** {proj.timeframe}")
            
            if proj.assumptions_stated:
                lines.append("**Stated Assumptions:**")
                for assumption in proj.assumptions_stated:
                    lines.append(f"- {assumption}")
            
            if proj.supporting_evidence:
                lines.append("**Supporting Evidence:**")
                for evidence in proj.supporting_evidence:
                    lines.append(f"- {evidence}")
            
            if proj.realism_assessment:
                lines.append(f"**Realism Assessment:** {proj.realism_assessment}")
            
            if proj.flags:
                lines.append("**⚠️ Flags/Concerns:**")
                for flag in proj.flags:
                    lines.append(f"- {flag}")
            
            lines.append("")
    
    # Facts vs Storytelling
    lines.append("---\n")
    lines.append("## 🔬 Facts vs. Storytelling\n")
    lines.append("*Distinguishing verifiable facts from marketing narrative and aspirational claims.*\n")
    
    if analysis.facts:
        lines.append("### ✅ Verifiable Facts")
        lines.append("*Claims with specific evidence or verification:*")
        for fact in analysis.facts:
            lines.append(f"- {fact}")
        lines.append("")
    
    if analysis.storytelling:
        lines.append("### 📖 Storytelling & Marketing Claims")
        lines.append("*Narrative elements, aspirational language, or claims without specific evidence:*")
        for story in analysis.storytelling:
            lines.append(f"- {story}")
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
    
    # Unconventional Data
    if analysis.unconventional_data:
        lines.append("---\n")
        lines.append("## 🔮 Unconventional & Additional Data\n")
        lines.append("*Information that doesn't fit standard categories but provides valuable context.*\n")
        
        # Group by category
        by_category = {}
        for item in analysis.unconventional_data:
            cat = item.category.replace('_', ' ').title()
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(item)
        
        for category, items in by_category.items():
            lines.append(f"### {category}")
            for item in items:
                trust_icon = {
                    "explicit": "✅",
                    "inferred": "🔍",
                    "vague": "⚠️",
                    "unverifiable": "❓"
                }.get(item.trustworthiness, "")
                
                lines.append(f"**{trust_icon} [{item.trustworthiness.upper()}] {item.source}**")
                lines.append(f"> {item.content}")
                
                if item.context:
                    lines.append(f"*Context: {item.context}*")
                if item.notes:
                    lines.append(f"*Note: {item.notes}*")
                lines.append("")
    
    # Additional Insights
    if analysis.additional_insights:
        lines.append("---\n")
        lines.append("## 💡 Additional Insights\n")
        for insight in analysis.additional_insights:
            conf_icon = {"high": "✅", "medium": "🔍", "low": "⚠️"}.get(insight.confidence, "")
            lines.append(f"### {conf_icon} {insight.title}")
            lines.append(f"**Source:** {insight.source} | **Confidence:** {insight.confidence}\n")
            lines.append(insight.description)
            if insight.relevance:
                lines.append(f"\n*Relevance:* {insight.relevance}")
            if insight.flags:
                lines.append("\n**Flags:**")
                for flag in insight.flags:
                    lines.append(f"- ⚠️ {flag}")
            lines.append("")
    
    # Text-Heavy Sections
    if analysis.text_heavy_sections:
        lines.append("---\n")
        lines.append("##     Detailed Content Sections\n")
        for section in analysis.text_heavy_sections:
            trust_icon = {
                "explicit": "✅",
                "inferred": "🔍",
                "vague": "⚠️",
                "unverifiable": "❓"
            }.get(section.trustworthiness, "")
            
            slides = ", ".join([f"#{n}" for n in section.slide_numbers]) if section.slide_numbers else "Unknown"
            lines.append(f"### {trust_icon} {section.title}")
            lines.append(f"**Slides:** {slides} | **Type:** {section.data_type} | **Trust:** {section.trustworthiness}\n")
            lines.append(section.content)
            
            if section.key_takeaways:
                lines.append("\n**Key Takeaways:**")
                for takeaway in section.key_takeaways:
                    lines.append(f"- {takeaway}")
            
            if section.notes:
                lines.append(f"\n*Note: {section.notes}*")
            lines.append("")
    
    # Customer Evidence
    if analysis.customer_testimonials or analysis.case_studies or analysis.pilot_programs:
        lines.append("---\n")
        lines.append("## 🗣️ Customer Evidence & Validation\n")
        
        if analysis.customer_testimonials:
            lines.append("### Customer Testimonials")
            for testimonial in analysis.customer_testimonials:
                lines.append(f"- {testimonial}")
            lines.append("")
        
        if analysis.case_studies:
            lines.append("### Case Studies")
            for case in analysis.case_studies:
                lines.append(f"- {case}")
            lines.append("")
        
        if analysis.pilot_programs:
            lines.append("### Pilot Programs")
            for pilot in analysis.pilot_programs:
                lines.append(f"- {pilot}")
            lines.append("")
    
    # Market & Industry Data
    if analysis.market_insights or analysis.industry_statistics:
        lines.append("---\n")
        lines.append("## 📊 Market & Industry Insights\n")
        
        if analysis.market_insights:
            lines.append("### Market Insights")
            for insight in analysis.market_insights:
                lines.append(f"- {insight}")
            lines.append("")
        
        if analysis.industry_statistics:
            lines.append("### Industry Statistics (Third-Party)")
            for stat in analysis.industry_statistics:
                lines.append(f"- {stat}")
            lines.append("")
    
    # Go-to-Market Details
    if analysis.gtm_strategy_details or analysis.marketing_channels or analysis.sales_strategy:
        lines.append("---\n")
        lines.append("## 🚀 Go-to-Market Strategy\n")
        
        if analysis.gtm_strategy_details:
            lines.append("### Strategy Overview")
            lines.append(f"{analysis.gtm_strategy_details}\n")
        
        if analysis.marketing_channels:
            lines.append("### Marketing Channels")
            for channel in analysis.marketing_channels:
                lines.append(f"- {channel}")
            lines.append("")
        
        if analysis.sales_strategy:
            lines.append("### Sales Strategy")
            lines.append(f"{analysis.sales_strategy}\n")
    
    # Technology & Product
    if analysis.technology_stack or analysis.technical_approach or analysis.product_roadmap or analysis.integration_partners:
        lines.append("---\n")
        lines.append("## 🔧 Technology & Product Details\n")
        
        if analysis.technology_stack:
            lines.append("### Technology Stack")
            for tech in analysis.technology_stack:
                lines.append(f"- {tech}")
            lines.append("")
        
        if analysis.technical_approach:
            lines.append("### Technical Approach")
            lines.append(f"{analysis.technical_approach}\n")
        
        if analysis.product_roadmap:
            lines.append("### Product Roadmap")
            for item in analysis.product_roadmap:
                lines.append(f"- {item}")
            lines.append("")
        
        if analysis.integration_partners:
            lines.append("### Integration Partners")
            for partner in analysis.integration_partners:
                lines.append(f"- {partner}")
            lines.append("")
    
    # Risks & Challenges
    if analysis.risks_acknowledged or analysis.mitigation_strategies:
        lines.append("---\n")
        lines.append("## ⚠️ Risks & Mitigation\n")
        
        if analysis.risks_acknowledged:
            lines.append("### Risks Acknowledged")
            for risk in analysis.risks_acknowledged:
                lines.append(f"- {risk}")
            lines.append("")
        
        if analysis.mitigation_strategies:
            lines.append("### Mitigation Strategies")
            for strategy in analysis.mitigation_strategies:
                lines.append(f"- {strategy}")
            lines.append("")
    
    # Media & Press
    if analysis.press_coverage or analysis.thought_leadership:
        lines.append("---\n")
        lines.append("## 📰 Media & Press\n")
        
        if analysis.press_coverage:
            lines.append("### Press Coverage")
            for press in analysis.press_coverage:
                lines.append(f"- {press}")
            lines.append("")
        
        if analysis.thought_leadership:
            lines.append("### Thought Leadership")
            for item in analysis.thought_leadership:
                lines.append(f"- {item}")
            lines.append("")
    
    # Present vs Missing Elements
    lines.append("---\n")
    lines.append("## ✅ Deck Completeness\n")
    
    if analysis.deck_quality_assessment:
        lines.append("### Overall Assessment")
        lines.append(f"{analysis.deck_quality_assessment}\n")
    
    if analysis.notable_strengths:
        lines.append("### Notable Strengths")
        for strength in analysis.notable_strengths:
            lines.append(f"- ✅ {strength}")
        lines.append("")
    
    if analysis.notable_weaknesses:
        lines.append("### Notable Weaknesses")
        for weakness in analysis.notable_weaknesses:
            lines.append(f"- ⚠️ {weakness}")
        lines.append("")
    
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
            
            if slide.additional_content:
                lines.append(f"**Additional Content:** {slide.additional_content}")
            
            if slide.data_items:
                lines.append("**Data Items:**")
                for item in slide.data_items:
                    lines.append(f"- {item}")
            
            lines.append("")
    
    return "\n".join(lines)
