# Metric Extraction Guidelines

## Philosophy: Facts Over Persuasion

This analysis tool extracts **EXPLICIT, LABELED FACTS ONLY**. It does not infer, assume, or be persuaded by the pitch deck's claims.

## ✅ What Gets Extracted as Facts

### Explicitly Labeled Metrics

| Category | Valid Examples | Invalid Examples |
|----------|---------------|------------------|
| **Funding** | "Seed Funding: $1.5M"<br>"Series A: $5M"<br>"Total Raised: $2M" | "Raised $1.5M" (no stage)<br>"Well-funded" |
| **MRR/ARR** | "MRR: $50K"<br>"ARR: $600K" | "Making $50K/month"<br>"Revenue growing" |
| **Users** | "10,000 Active Users"<br>"500 Paying Customers" | "Thousands of users"<br>"Growing user base" |
| **Market Size** | "TAM: $5B"<br>"SAM: $500M"<br>"SOM: $50M" | "Large market"<br>"Billion dollar opportunity" |
| **LOIs** | "3 LOIs"<br>"LOI Total Value: $750K" | "Multiple LOIs"<br>"Strong pipeline" |
| **Growth** | "MoM Growth: 15%"<br>"YoY Growth: 200%" | "Rapid growth"<br>"Hockey stick" |
| **Churn** | "Churn Rate: 2%"<br>"Monthly Churn: 1.5%" | "Low churn"<br>"Sticky product" |
| **Unit Economics** | "LTV: $5,000"<br>"CAC: $500"<br>"LTV/CAC: 10x" | "Great unit economics" |

## 🔍 How Different Claims Are Handled

### 1. Explicitly Labeled → Facts
**Deck says:** "Seed Funding: $1.5M raised in Q1 2024"

**Extracted:**
```json
{
  "metrics": {
    "funding": [
      {
        "label": "Seed Funding",
        "value": "$1.5M",
        "context": "Raised in Q1 2024",
        "is_projection": false
      }
    ]
  }
}
```

### 2. Unlabeled → Observations
**Deck says:** "Raised $1.5M last year"

**Extracted:**
```json
{
  "unlabeled_claims": [
    "States raised $1.5M but does not specify funding stage (seed, Series A, etc.)"
  ],
  "metrics": {
    "funding": [
      {
        "label": "Funding (stage unspecified)",
        "value": "$1.5M",
        "context": "Last year",
        "is_projection": false
      }
    ]
  }
}
```

### 3. Vague Claims → Flagged
**Deck says:** "Significant revenue growth"

**Extracted:**
```json
{
  "unlabeled_claims": [
    "Claims 'significant revenue growth' without specific percentage or timeframe"
  ]
}
```

### 4. Projections → Marked
**Deck says:** "Projected ARR: $2M by EOY 2025"

**Extracted:**
```json
{
  "metrics": {
    "financials": [
      {
        "label": "ARR Projection",
        "value": "$2M",
        "context": "By end of 2025",
        "is_projection": true
      }
    ]
  }
}
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
