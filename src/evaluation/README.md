# Investment Evaluation Pipeline

## Overview
This pipeline evaluates startups from a **critical VC perspective**, scoring companies on 6 key criteria to identify potential unicorns and avoid poor investments.

## VC Philosophy

### Core Principles
- **High bar for scoring**: Most companies score 2-3. Only exceptional companies deserve 4-5.
- **Market size is critical**: TAM <$1B is a deal-breaker. We need billion-dollar outcomes.
- **Growth metrics matter**: Revenue growth, unit economics, and burn rate are scrutinized.
- **Be objective but demanding**: Good is good, bad is bad. No sugarcoating.

### What VCs Look For
1. **Billion-dollar potential**: Can this be a unicorn (>$1B valuation)?
2. **3-5x returns**: Investment must have potential for significant multiple
3. **Exceptional teams**: Founders with track record, domain expertise, complementary skills
4. **Defensible moats**: Sustainable competitive advantages
5. **Large markets**: TAM >$10B preferred, minimum $1B
6. **Strong traction**: Revenue growth >3x YoY, improving unit economics

## Scoring Criteria (1-5 Scale)

### 1. Team
- **1**: Solo founder, no relevant experience, or weak team
- **2**: Small team with limited track record
- **3**: Competent team with relevant experience but no proven exits
- **4**: Strong team with domain expertise, prior startup experience, or 1 exit
- **5**: Exceptional team with multiple successful exits

**Red flags**: First-time founders without advisors, missing key roles, team imbalances

### 2. Technology
- **1**: Just an idea or concept
- **2**: Early MVP or prototype
- **3**: Working product with early users but limited scalability
- **4**: Production product with proven scalability and some moat
- **5**: Market-leading technology with strong IP or proprietary data

**Red flags**: Non-proprietary tech, easily replicable, outdated stack

### 3. Market (CRITICAL)
- **1**: TAM <$1B (too small for VC scale)
- **2**: TAM $1-5B (small for venture scale)
- **3**: TAM $5-20B (acceptable but needs dominant share)
- **4**: TAM $20-50B (large market with growth)
- **5**: TAM >$50B (massive market with secular tailwinds)

**Be ruthless**: Anything under $1B TAM is automatic concern. Question inflated calculations.

### 4. Value Proposition
- **1**: Weak problem-solution fit, "vitamin" not "painkiller"
- **2**: Addresses minor pain point, unclear willingness to pay
- **3**: Solves real problem but competitive or incremental
- **4**: Clear painkiller with strong differentiation
- **5**: 10x better solution, creates new category

**Red flags**: "Nice to have" products, unclear ROI

### 5. Competitive Advantage (MOAT)
- **1**: No moat, commodity product
- **2**: Weak defensibility, first-mover advantage only
- **3**: Some moat (brand, switching costs) but vulnerable
- **4**: Strong moat (network effects, data moat, IP)
- **5**: Multiple compounding moats, near-impossible to replicate

**Critical**: Without a moat, even great execution gets competed away

### 6. Social Impact
- **1**: No social impact or potentially negative
- **2**: Minor positive impact, limited scope
- **3**: Moderate impact in specific area
- **4**: Significant impact addressing important challenge
- **5**: Transformative impact on critical global problem

**Note**: Important for ESG but secondary to returns for most VCs

## Growth Metrics - Critical Benchmarks

### Revenue
- **<$100K MRR** after 2+ years: Concerning
- **$50K MRR** after 4 years: **RED FLAG**
- **Growth <50% YoY**: Weak
- **Growth >3x YoY**: Strong
- **Flat growth**: Failing

### Unit Economics
- **CAC payback >24 months**: Concerning
- Need clear path to profitability
- LTV:CAC ratio should be >3:1

### Burn & Runway
- **Runway <12 months** without clear revenue ramp: Risky
- High burn without corresponding growth: Red flag

## Projections - Haircut Aggressively

Most projections are overly optimistic:
- **Haircut by 50-70%** for aggressive forecasts
- Question assumptions: CAC, conversion rates, market penetration
- **Red flag**: Hockey stick without historical validation

## Output Format

The evaluation produces `evaluation.md` with:
1. **Summary Table**: All 6 scores at a glance
2. **Detailed Scores**: Each criterion with reasoning
3. **Competitor Analysis**: Grouped by category (not redundant lists)
4. **Critical Comments**: Revenue metrics, red flags, VC fit, unicorn potential

## Usage

```python
from src.evaluation.main import evaluate_company_analysis

# Evaluate a company
success = evaluate_company_analysis(
    company_name="acme-corp",
    company_output_dir="output/acme-corp"
)
```

## Example Scores

### Weak Company (Avg: 2.0)
- Team: 2 (First-time founder, small team)
- Technology: 2 (Early MVP)
- Market: 1 (TAM $500M)
- Value Prop: 3 (Solves problem but competitive)
- MOAT: 2 (Weak defensibility)
- Impact: 2 (Minor)
- **Verdict**: Pass. Too small market, weak team, no moat.

### Strong Company (Avg: 4.2)
- Team: 4 (Experienced founders with 1 exit)
- Technology: 5 (Proprietary AI with strong IP)
- Market: 5 (TAM $80B, growing 20% YoY)
- Value Prop: 4 (10x faster than alternatives)
- MOAT: 4 (Network effects + data moat)
- Impact: 3 (Moderate)
- **Verdict**: Strong candidate. Large market, differentiated tech, experienced team.

## Key Differentiators from Founder Perspective

| Aspect | Founder View | VC View |
|--------|--------------|---------|
| Market size | "Large enough" | Must be >$1B, prefer >$10B |
| Growth | 50% YoY = good | Need >3x YoY for venture scale |
| Competition | "We're different" | "What's your sustainable moat?" |
| Revenue | Any revenue = traction | <$100K MRR after 2yr = concern |
| Team | "We're passionate" | "Do you have exits and expertise?" |
| Projections | Optimistic | Haircut 50-70%, prove it |

## Remember

You're protecting LP capital and seeking outlier returns. Be tough, be fair, be objective. A score of 3 is average. Most companies are 2-3. Reserve 4-5 for truly exceptional attributes.
