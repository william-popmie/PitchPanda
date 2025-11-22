"""Markdown rendering for web analysis results."""

from .schemas import Analysis, Competitor


# ---------- helpers ----------
def _render_locations(locs):
    return "- None specified" if not locs else "\n".join(f"- {x}" for x in locs)


def _bullets(items):
    return "- None" if not items else "\n".join(f"- {x}" for x in items)


def _truncate(s: str, n: int = 180) -> str:
    s = (s or "").strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


# ---------- one-liner clipboard helpers ----------
def _one_liner_for_competitor(target_product_type: str, c: Competitor) -> str:
    c = c if isinstance(c, Competitor) else Competitor(**c)
    name = (c.name or "Unknown").strip()

    # Same / different product type tag
    tpt = (target_product_type or "").strip().lower()
    cpt = (c.product_type or "").strip().lower()
    if cpt and tpt and cpt == tpt:
        sol_tag = "same product type"
    elif c.product_type:
        sol_tag = f"different product type ({c.product_type})"
    else:
        sol_tag = "solution unspecified"

    # Prefer first difference → similarity → solution summary
    note = (c.differences[0] if c.differences else "") or \
           (c.similarities[0] if c.similarities else "") or \
           (c.solution_summary or "")

    geo = ", ".join(c.active_locations) if c.active_locations else "n/a"
    return f"{name}: same problem; {sol_tag}; {_truncate(note)}; geo: {geo}"


def render_competition_clipboard(target_product_type: str, competitors: list[Competitor]) -> str:
    if not competitors:
        return "(no competitors found)"
    lines = [
        _one_liner_for_competitor(target_product_type, c if isinstance(c, Competitor) else Competitor(**c))
        for c in competitors
    ]
    return "\n".join(lines)


# ---------- structured competition ----------
def _render_competitor(c: Competitor) -> str:
    c = c if isinstance(c, Competitor) else Competitor(**c)
    locs = _render_locations(c.active_locations)
    srcs = "- None\n" if not c.sources else "\n".join(f"- {s}" for s in c.sources)
    website_line = f"**Website:** {c.website}\n" if c.website else ""
    prod_line = f"**Product type:** {c.product_type or 'Unknown'}\n"
    sect_line = f"**Sector/Subsector:** {c.sector or 'Unknown'} / {c.subsector or 'Unknown'}\n"
    
    # Confidence badge
    confidence_emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(c.confidence.lower() if c.confidence else "medium", "🟡")
    confidence_line = f"**Confidence:** {confidence_emoji} {c.confidence or 'Medium'}\n"
    
    why_line = f"**Why included:** {c.why_included}\n" if c.why_included else ""
    
    sims = _bullets(c.similarities)
    diffs = _bullets(c.differences)
    return f"""### {c.name}
{website_line}{prod_line}{sect_line}{confidence_line}{why_line}
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


# ---------- main markdown ----------
def render_markdown(name: str, url: str, a: Analysis) -> str:
    # Market size section
    if a.market_size:
        market_section = f"""## 📊 Market Size Estimate

### Total Addressable Market (TAM)
**Value:** {a.market_size.tam.value}

**Formula:**
```
{a.market_size.tam.formula}
```

**Assumptions:**
{_bullets(a.market_size.tam.assumptions)}

**Unit:** {a.market_size.tam.unit}

---

### Serviceable Addressable Market (SAM)
**Value:** {a.market_size.sam.value}

**Formula:**
```
{a.market_size.sam.formula}
```

**Assumptions:**
{_bullets(a.market_size.sam.assumptions)}

**Unit:** {a.market_size.sam.unit}

---

### Serviceable Obtainable Market (SOM)
**Value:** {a.market_size.som.value}

**Formula:**
```
{a.market_size.som.formula}
```

**Assumptions:**
{_bullets(a.market_size.som.assumptions)}

**Unit:** {a.market_size.som.unit}

---

**Calculation Note:**
{a.market_size.calculation_note}
"""
    else:
        market_section = ""

    # Structured competition
    if a.competition:
        comp_section = "\n\n".join(
            _render_competitor(Competitor(**c)) if not isinstance(c, Competitor)
            else _render_competitor(c)
            for c in a.competition
        )
    else:
        comp_section = "No competitors found."

    # Copy-paste one-liners
    clipboard_block = render_competition_clipboard(a.product_type, a.competition)

    # Final Markdown document
    return f"""# {name}

**Website:** {url}

## 📝 Summary

{a.company_summary}

---

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

{market_section}
## Competition (Structured)
{comp_section}

## Competition (Copy-paste one-liners)
{clipboard_block}

## Sources
{chr(10).join(f"- {s}" for s in a.sources)}
"""
