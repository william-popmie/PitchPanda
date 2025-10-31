from .schemas import Analysis, Competitor
from .utils import hostname

def _render_locations(locs):
    return "- None specified" if not locs else "\n".join(f"- {x}" for x in locs)

def _render_competitor(c: Competitor) -> str:
    locs = _render_locations(c.active_locations)
    srcs = "- None\n" if not c.sources else "\n".join(f"- {s}" for s in c.sources)
    website_line = f"**Website:** {c.website}\n" if c.website else ""
    prod_line = f"**Product type:** {c.product_type or 'Unknown'}\n"
    sect_line = f"**Sector/Subsector:** {c.sector or 'Unknown'} / {c.subsector or 'Unknown'}\n"
    sims = "\n".join(f"- {s}" for s in (c.similarities or [])) or "- None listed"
    diffs = "\n".join(f"- {d}" for d in (c.differences or [])) or "- None listed"
    return f"""### {c.name}
{website_line}{prod_line}{sect_line}
**Problem similarity:** {c.problem_similarity}

**Solution summary:** {c.solution_summary}

**Similarities**
{sims}

**Differences**
{diffs}

**Active Locations**
{locs}

**Sources**
{srcs}
"""

def render_markdown(name: str, url: str, a: Analysis) -> str:
    comp_section = "No competitors found."
    if a.competition:
        comp_section = "\n\n".join(_render_competitor(Competitor(**c)) if not isinstance(c, Competitor) else _render_competitor(c) for c in a.competition)

    return f"""# {name}

**Website:** {url}

## Problem
**General:** {a.problem.general}
**Example:** {a.problem.example}

## Solution
**Product:** {a.solution.what_it_is}
**How it works:** {a.solution.how_it_works}
**Example:** {a.solution.example}

## Product Type
{a.product_type}

## Sector
**Sector:** {a.sector}  
**Subsector:** {a.subsector}

## Active Locations
{_render_locations(a.active_locations)}

## Competition
{comp_section}

## Sources
{chr(10).join(f"- {s}" for s in a.sources)}
"""
