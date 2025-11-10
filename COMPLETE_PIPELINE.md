# Complete Pipeline Overview

## 🎯 Three-Stage Analysis Pipeline

PitchPanda now runs a complete three-stage pipeline that generates comprehensive company overviews:

```
                    INPUT
                      ↓
        ┌─────────────┴─────────────┐
        ↓                           ↓
   pitches.csv              input/decks/*.pdf
        ↓                           ↓
        │                           │
        ↓                           ↓
┌───────────────┐         ┌──────────────┐
│ WEB ANALYSIS  │         │ DECK ANALYSIS│
└───────┬───────┘         └──────┬───────┘
        │                        │
        │   web_analysis.md      │ deck_analysis.md
        │                        │
        └────────┬───────────────┘
                 ↓
        ┌────────────────┐
        │ MERGE ANALYSIS │
        └────────┬───────┘
                 ↓
          merged_analysis.md ⭐
             (COMPREHENSIVE)
```

## Pipeline Stages

### Stage 1: Web Analysis 🌐
**Input:** Company URL from CSV  
**Output:** `web_analysis.md`  
**Contains:**
- Problem & solution (with real-world examples)
- Market size analysis (TAM/SAM/SOM)
- Competitor research
- Product type & sector classification

### Stage 2: Deck Analysis 🎯
**Input:** PDF file from `input/decks/`  
**Output:** `deck_analysis.md`  
**Contains:**
- Detailed pitch elements
- Team information
- Financial metrics & projections
- Competitive advantages & IP
- Facts vs. storytelling analysis

### Stage 3: Merge Analysis 🔀
**Input:** Both analyses from stages 1 & 2  
**Output:** `merged_analysis.md` ⭐  
**Contains:**
- **Everything from both sources combined**
- Source attribution on every data point
- Conflict handling when sources disagree
- Web examples shown first, then pitch deck details
- Complete company overview in one document

## Key Features

### 1. Source Attribution
Every piece of information is clearly marked:
- `*(web analysis)*` - From web scraping
- `*(pitch deck)*` - From pitch deck
- `*(pitch deck & web analysis)*` - Found in both

### 2. Conflict Resolution
When sources provide different data:
```markdown
**Total Addressable Market:**
- **Pitch Deck**: $6.2B by 2036
- **Web Analysis**: $1.5B - $3B annually
```

### 3. Structured Problem/Solution
Shows web context first (more accessible), then pitch deck details:
```markdown
### Problem
**General:** [Web description] *(web analysis)*
**Example:** [Real scenario] *(web analysis)*
**Additional Details:** [Pitch deck specifics] *(pitch deck)*
```

### 4. Graceful Degradation
Pipeline continues even with missing data:
- No URL? → Skip web, run deck + merge
- No PDF? → Skip deck, run web + merge
- Only one source? → Merge still works!

## Usage

### Run Complete Pipeline
```bash
python -m src.main
```

This automatically runs all three stages for every company in `input/pitches.csv`.

### Run Individual Stages
```bash
# Stage 1: Web only
python -m src.web_analysis.main

# Stage 2: Deck only
python -m src.deck_analysis.main

# Stage 3: Merge only (requires existing analyses)
python -m src.merge_analysis.main
```

## Output Structure

```
output/
└── company-name/
    ├── web_analysis.md      # Stage 1 output
    ├── deck_analysis.md     # Stage 2 output
    └── merged_analysis.md   # Stage 3 output ⭐ (FINAL)
```

## The Final Document

`merged_analysis.md` is your **comprehensive company overview** containing:

1. 📋 **Company Overview** - Name, website, sector, locations
2. 🎯 **Problem & Solution** - Web examples + pitch deck details
3. 📊 **Market Information** - TAM/SAM/SOM with conflict handling
4. 💼 **Business Model** - Revenue, pricing, partnerships
5. 👥 **Team** - Complete team from both sources
6. 💰 **Financial Data** - Funding, revenue, traction, projections
7. 🏆 **Competition** - All competitors with analysis
8. 🛡️ **Competitive Advantages** - IP, patents, unique tech
9. 🔧 **Technology** - Technical details
10. 🚀 **Go-to-Market** - Strategy and execution
11. 🏅 **Awards** - Recognition and grants
12. 💬 **Customer Evidence** - Testimonials and validation
13. 💡 **Additional Insights** - Everything else

## Why Three Stages?

### Web Analysis Provides:
- ✅ Public-facing messaging
- ✅ Real-world examples
- ✅ Market context
- ✅ Competitive landscape
- ✅ Accessible problem/solution

### Deck Analysis Provides:
- ✅ Detailed metrics
- ✅ Team backgrounds
- ✅ Financial projections
- ✅ IP portfolio
- ✅ Strategic plans

### Merge Analysis Provides:
- ✅ **Complete picture**
- ✅ **Source transparency**
- ✅ **Conflict awareness**
- ✅ **One comprehensive document**
- ✅ **Everything in context**

## Best Practices

1. **Start with main pipeline** - Let it run all three stages
2. **Focus on merged_analysis.md** - It's the definitive overview
3. **Check source attributions** - Know where each fact comes from
4. **Review conflicts** - Understand differences between sources
5. **Keep originals** - web_analysis.md and deck_analysis.md preserved

## Requirements

- Python environment with dependencies installed
- OpenAI API key in `.env` or environment
- CSV with company names and URLs
- PDFs in `input/decks/` (optional but recommended)

---

**Result:** One comprehensive, source-attributed, conflict-aware document per company that combines everything! 🎉
