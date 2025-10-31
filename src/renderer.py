from .schemas import Analysis
from .utils import hostname

def render_markdown(name: str, url: str, a: Analysis) -> str:
    loc_lines = "- None specified"
    if a.active_locations:
        loc_lines = "\n".join(f"- {x}" for x in a.active_locations)

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
{loc_lines}

## Sources
{chr(10).join(f"- {s}" for s in a.sources)}
"""
