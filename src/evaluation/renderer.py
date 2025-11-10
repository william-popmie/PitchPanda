"""
Renderer for company evaluation.
"""
from .schemas import CompanyEvaluation, Criterion, CompetitorGroup


def render_criterion(criterion: Criterion) -> str:
    """Render a single criterion score."""
    stars = "★" * criterion.score + "☆" * (5 - criterion.score)
    return f"**{criterion.name}:** {criterion.score}/5 {stars}\n{criterion.reasoning}\n"


def render_evaluation(evaluation: CompanyEvaluation) -> str:
    """
    Render the evaluation to markdown format.
    
    Args:
        evaluation: CompanyEvaluation object
        
    Returns:
        Markdown formatted string
    """
    lines = []
    
    # Header
    lines.append(f"# Investment Evaluation: {evaluation.company_name}")
    lines.append("")
    lines.append(f"**Overall Score: {evaluation.overall_score:.1f}/5.0**")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Individual Scores
    lines.append("## 📊 Evaluation Criteria")
    lines.append("")
    
    lines.append("### 1. Team")
    lines.append(render_criterion(evaluation.team))
    
    lines.append("### 2. Technology")
    lines.append(render_criterion(evaluation.technology))
    
    lines.append("### 3. Market Size")
    lines.append(render_criterion(evaluation.market))
    
    lines.append("### 4. Value Proposition")
    lines.append(render_criterion(evaluation.value_proposition))
    
    lines.append("### 5. Competitive Advantage (MOAT)")
    lines.append(render_criterion(evaluation.competitive_advantage))
    
    lines.append("### 6. Social Impact")
    lines.append(render_criterion(evaluation.social_impact))
    
    lines.append("---")
    lines.append("")
    
    # Score Summary Table
    lines.append("## 📈 Score Summary")
    lines.append("")
    lines.append("| Criterion | Score | Rating |")
    lines.append("|-----------|-------|--------|")
    lines.append(f"| Team | {evaluation.team.score}/5 | {'★' * evaluation.team.score}{'☆' * (5 - evaluation.team.score)} |")
    lines.append(f"| Technology | {evaluation.technology.score}/5 | {'★' * evaluation.technology.score}{'☆' * (5 - evaluation.technology.score)} |")
    lines.append(f"| Market Size | {evaluation.market.score}/5 | {'★' * evaluation.market.score}{'☆' * (5 - evaluation.market.score)} |")
    lines.append(f"| Value Proposition | {evaluation.value_proposition.score}/5 | {'★' * evaluation.value_proposition.score}{'☆' * (5 - evaluation.value_proposition.score)} |")
    lines.append(f"| Competitive Advantage | {evaluation.competitive_advantage.score}/5 | {'★' * evaluation.competitive_advantage.score}{'☆' * (5 - evaluation.competitive_advantage.score)} |")
    lines.append(f"| Social Impact | {evaluation.social_impact.score}/5 | {'★' * evaluation.social_impact.score}{'☆' * (5 - evaluation.social_impact.score)} |")
    lines.append(f"| **Overall** | **{evaluation.overall_score:.1f}/5** | **{'★' * int(round(evaluation.overall_score))}{'☆' * (5 - int(round(evaluation.overall_score)))}** |")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Competitive Landscape
    if evaluation.competitor_groups:
        lines.append("## 🏆 Competitive Landscape")
        lines.append("")
        
        for group in evaluation.competitor_groups:
            lines.append(f"### {group.group_name}")
            lines.append(f"**Competitors:** {', '.join(group.competitors)}")
            lines.append("")
            lines.append(f"**Characteristics:** {group.characteristics}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Final Comments
    lines.append("## 💭 Final Comments & Observations")
    lines.append("")
    lines.append(evaluation.comments)
    lines.append("")
    
    return "\n".join(lines)
