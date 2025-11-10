# PitchPanda - Main Pipeline Usage

## Quick Start

Run the complete analysis pipeline on all companies in your CSV:

```bash
python -m src.main
```

This will automatically:
1. 🌐 **Web Analysis** - Scrape and analyze company websites
2. 🎯 **Deck Analysis** - Analyze pitch deck PDFs
3. 🔀 **Merge Analysis** - Combine both into comprehensive overview ⭐

## Complete Pipeline Flow

```
input/pitches.csv → [Companies]
                         ↓
                    Web Analysis
                         ↓
                    Deck Analysis  
                         ↓
                    Merge Analysis
                         ↓
output/company-name/
├── web_analysis.md      # Web data
├── deck_analysis.md     # Pitch deck data
└── merged_analysis.md   # ⭐ COMPREHENSIVE OVERVIEW
```

## Setup

### 1. Prepare Input Files

**CSV File:** `input/pitches.csv`
```csv
startup_name,startup_url
DeFloria,https://defloria.bio/
My Town AI,https://mytownai.com/
```

**PDF Files:** `input/decks/`
```
input/decks/
├── defloria.pdf
├── my-town-ai.pdf
└── ...
```

### 2. Set Environment Variables

Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Pipeline

```bash
# Run on all companies in pitches.csv
python -m src.main

# Or specify a custom CSV
python -m src.main path/to/custom.csv
```

## Output Structure

After running, you'll get:

```
output/
├── defloria/
│   ├── web_analysis.md      # Web scraping results
│   ├── deck_analysis.md     # Pitch deck analysis
│   └── merged_analysis.md   # ⭐ Complete company overview
├── my-town-ai/
│   ├── web_analysis.md
│   ├── deck_analysis.md
│   └── merged_analysis.md
└── ...
```

## What Gets Generated

### 1. Web Analysis (`web_analysis.md`)
- Problem & Solution (with examples)
- Product Type & Sector
- Market Size (TAM/SAM/SOM)
- Competition Analysis
- Active Locations

### 2. Deck Analysis (`deck_analysis.md`)
- Core pitch elements
- Metrics & numbers
- Team information
- Competitive advantages & IP
- Funding breakdown
- Projections analysis
- Facts vs. storytelling

### 3. Merged Analysis (`merged_analysis.md`) ⭐

**The comprehensive overview combining everything:**

- 📋 Company Overview
- 🎯 Problem & Solution (web examples + deck details)
- 📊 Market Information (with conflict handling)
- 💼 Business Model
- 👥 Complete Team
- 💰 Financial Data & Traction
- 🏆 Competitive Landscape
- 🛡️ Competitive Advantages & IP
- � Technology Details
- � Go-to-Market Strategy
- 🏅 Awards & Recognition
- 💬 Customer Evidence
- 💡 Additional Insights

**Key Features:**
- ✅ Source attribution on every data point: `*(pitch deck)* ` `*(web analysis)* ` `*(both)*`
- ✅ Conflict handling when sources disagree
- ✅ Clear marking of missing information
- ✅ Web examples shown first, then pitch deck details

## Handling Missing Data

The pipeline gracefully handles missing inputs:

- **No URL?** → Skips web analysis, continues with deck
- **No PDF?** → Skips deck analysis, continues with web
- **Only one source?** → Merge analysis still runs with available data
- **Both missing?** → Skips that company

## Running Individual Pipelines

You can also run pipelines separately:

```bash
# Web analysis only
python -m src.web_analysis.main

# Deck analysis only
python -m src.deck_analysis.main

# Merge analysis only (requires existing analyses)
python -m src.merge_analysis.main
```

## Tips

1. **Start with small batches** - Test with 1-2 companies first
2. **Check API limits** - The pipeline uses OpenAI API extensively
3. **PDF naming** - Name PDFs to match company names (e.g., `defloria.pdf` for "DeFloria")
4. **Review merged_analysis.md** - This is your final comprehensive document ⭐

## Troubleshooting

**"Missing input CSV"**
- Ensure `input/pitches.csv` exists with correct headers

**"No PDF found"**
- Check file is in `input/decks/`
- Verify filename matches company name (slugified)

**"OpenAI API key error"**
- Set `OPENAI_API_KEY` in `.env` file or environment

**"No analyses completed"**
- Check if URL is valid and PDF exists
- At least one is required per company

## Example Output

After running the pipeline, each company gets a comprehensive merged analysis like:

```markdown
# DeFloria

## 🎯 Problem & Solution

### Problem
**General:** The autism community faces a critical shortage of effective 
therapeutic options... *(web analysis)*

**Example:** A parent of a child with ASD struggles to find medication... 
*(web analysis)*

**Additional Details:** Irritability associated with Autism Spectrum Disorder 
(ASD) with limited FDA-approved treatments... *(pitch deck)*

### Solution
Botanical cannabinoid drug - DeFloria is developing AJA001... *(web analysis)*

**Example:** A child with ASD begins taking AJA001... *(web analysis)*

**Additional Details:** AJA001, a botanical drug product derived from 
full-spectrum cannabinoid extract... *(pitch deck)*
```

---

**Ready to go!** Just run `python -m src.main` and let PitchPanda analyze everything! 🐼
