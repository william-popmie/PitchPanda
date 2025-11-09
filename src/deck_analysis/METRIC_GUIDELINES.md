# Metric Extraction Guidelines

## Philosophy: Capture All Numbers with Confidence Levels

This analysis tool extracts **ALL METRICS AND NUMBERS** from pitch decks, marking each with a confidence level to indicate how explicitly it was labeled.

### Key Principles:
1. **Extract everything** - Don't skip numbers even if vaguely labeled
2. **Mark confidence** - High/Medium/Low based on labeling clarity
3. **Add notes** - Flag unrealistic claims or uncertainty
4. **Go into detail** - Separate Seed/Series A/B/C, TAM/SAM/SOM, etc.
5. **Stay neutral** - Present facts, don't be persuaded

## ✅ Confidence Levels

### ⭐⭐⭐ High Confidence (Explicitly Labeled)
Metrics with clear, unambiguous labels:
- "Seed Funding: $1.5M" ✅
- "MRR: $25K" ✅
- "TAM: $10B" ✅
- "Churn Rate: 2%" ✅
- "LTV/CAC: 10x" ✅

### ⭐⭐ Medium Confidence (Inferred but Reasonable)
Metrics that can be reasonably inferred from context:
- "$1.5M raised in 2024" → Likely funding, mark as "Funding (stage uncertain)"
- "$25K monthly revenue" → Probably MRR, note "Not explicitly labeled as MRR"
- "10B market" → Likely TAM, note "TAM/SAM/SOM distinction unclear"
- "$500/customer acquisition" → Probably CAC, note inference

### ⭐ Low Confidence (Vague/Uncertain)
Numbers mentioned with unclear context:
- Chart with unlabeled axes showing numbers
- "Significant revenue" with nearby figure
- Timeframes not specified
- Source of number unclear

## 🔍 How Different Claims Are Handled

### 1. Explicitly Labeled → High Confidence
**Deck says:** "Seed Funding: $1.5M raised in Q1 2024"

**Extracted:**
```json
{
  "label": "Seed Funding",
  "value": "$1.5M",
  "context": "Raised in Q1 2024",
  "is_projection": false,
  "confidence": "high",
  "notes": null
}
```

### 2. Unlabeled but Clear → Medium Confidence
**Deck says:** "Raised $1.5M last year"

**Extracted:**
```json
{
  "label": "Funding (stage uncertain)",
  "value": "$1.5M",
  "context": "Last year",
  "is_projection": false,
  "confidence": "medium",
  "notes": "Funding stage not specified"
}
```

### 3. Vague Context → Low Confidence
**Deck says:** Chart showing "$2M" without clear labeling

**Extracted:**
```json
{
  "label": "Revenue (uncertain)",
  "value": "$2M",
  "context": "From slide 8 chart",
  "is_projection": false,
  "confidence": "low",
  "notes": "Context unclear - could be revenue, funding, or projection"
}
```

### 4. Unrealistic Claims → Noted
**Deck says:** "Projected Users: 100M by end of 2025" (current: 1,000 users)

**Extracted:**
```json
{
  "label": "Projected Users",
  "value": "100M",
  "context": "By end of 2025",
  "is_projection": true,
  "confidence": "high",
  "notes": "Extremely ambitious - 100,000x growth in 1 year seems unrealistic given current 1K users"
}
```

### 5. Detailed Breakdown → Separate Entries
**Deck says:** "Raised $3M: $1M seed (2023), $2M Series A (2024)"

**Extracted:**
```json
[
  {
    "label": "Seed Funding",
    "value": "$1M",
    "context": "2023",
    "is_projection": false,
    "confidence": "high",
    "notes": null
  },
  {
    "label": "Series A",
    "value": "$2M",
    "context": "2024",
    "is_projection": false,
    "confidence": "high",
    "notes": null
  },
  {
    "label": "Total Funding Raised",
    "value": "$3M",
    "context": "Cumulative",
    "is_projection": false,
    "confidence": "high",
    "notes": null
  }
]
```

## 🏢 Special Cases

### Competition
Competition mentioned in pitch decks is **inherently biased** (founder perspective). We extract it but note the bias:

```json
{
  "competition_mentioned": ["Competitor A", "Competitor B"],
  "competition_note": "Competition as presented in deck may be biased toward favorable comparison"
}
```

### Team Information
Extract factual backgrounds only:
- ✅ "Ex-Google Engineer"
- ✅ "Former Founder of TechCo (acquired by Y)"
- ✅ "10 years in SaaS sales"
- ❌ "Industry expert" (too vague)
- ❌ "Proven track record" (marketing language)

### Market Size
Only extract if TAM/SAM/SOM are explicitly labeled:
- ✅ "TAM: $10B" → Extract as fact
- ❌ "$10B market" → Is this TAM? SAM? Flag as unlabeled
- ❌ "Huge market opportunity" → Too vague, ignore

## 📊 Output Structure

The analysis separates:

1. **Metrics** (dict by category) - Only explicitly labeled facts
2. **Observations** - General notes about the deck
3. **Unlabeled Claims** - Claims that lack specificity
4. **Present Elements** - What IS in the deck
5. **Missing Elements** - What's NOT in the deck
6. **Data Quality Notes** - Assessment of labeling quality

## 🎯 Goal

Provide **objective, factual analysis** that:
- ✅ Respects explicit labels
- ✅ Distinguishes facts from projections
- ✅ Notes bias in competition claims
- ✅ Flags vague or unlabeled claims
- ❌ Does NOT infer or assume
- ❌ Does NOT be persuaded by marketing language
- ❌ Does NOT fill in missing labels

This approach gives investors/analysts **clean, factual data** to make their own judgments.
