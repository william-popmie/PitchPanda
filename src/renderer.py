from .schemas import Analysis
from .utils import hostname

def render_markdown(name: str, url: str, a: Analysis) -> str:
    host = hostname(url)
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

## Sources
{chr(10).join(f"- {s}" for s in a.sources)}
"""
