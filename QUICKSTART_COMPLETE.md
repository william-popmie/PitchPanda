# 🚀 Quick Start - Complete Pipeline

## One Command to Rule Them All

```bash
python -m src.main
```

This runs **everything**:
1. Web Analysis
2. Deck Analysis  
3. Merge Analysis ⭐

## What You Need

### 1. CSV File: `input/pitches.csv`
```csv
startup_name,startup_url
DeFloria,https://defloria.bio/
My Town AI,https://mytownai.com/
```

### 2. PDF Files: `input/decks/` (optional)
```
input/decks/
├── defloria.pdf
└── my-town-ai.pdf
```

### 3. Environment: `.env` file
```bash
OPENAI_API_KEY=your_key_here
```

## What You Get

```
output/
└── company-name/
    ├── web_analysis.md      
    ├── deck_analysis.md     
    └── merged_analysis.md   ⭐ ← READ THIS ONE!
```

## The Star of the Show: `merged_analysis.md`

**Complete company overview with:**
- ✅ ALL information from web + pitch deck
- ✅ Source tags: `*(web analysis)*` or `*(pitch deck)*`
- ✅ Conflicts clearly shown when sources disagree
- ✅ Web examples first, then deck details
- ✅ Everything in one place

## That's It! 

Just run `python -m src.main` and get comprehensive company analyses for everyone in your CSV.

---

**Pro tip:** Start with 1-2 companies in your CSV to test, then scale up!
