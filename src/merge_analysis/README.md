# Merge Analysis Pipeline

The merge analysis pipeline combines information from both the pitch deck analysis and web analysis into a comprehensive company overview document.

## Overview

This pipeline creates a unified view of a company by:
- Merging all available information from both sources
- Clearly attributing each piece of information to its source (pitch deck, web analysis, or both)
- Handling conflicting information by showing both versions
- Marking missing information clearly
- Preserving all important details without summarization

## Usage

### Run on all companies

```bash
python -m src.merge_analysis.main
```

This will process all company folders in the `output/` directory that have either `deck_analysis.md` or `web_analysis.md` (or both).

### Run on a specific company

```bash
python -m src.merge_analysis.main output/company-name
```

## Output

For each company, the pipeline generates `merged_analysis.md` in the company's output folder with the following sections:

### 📋 Company Overview
- Name, website, tagline, description
- Sector and locations
- All sourced from available analyses

### 🎯 Problem & Solution
- Problem statement
- Solution overview
- Value proposition
- Product type
- How it works

### 📊 Market Information
- Target market description
- TAM (Total Addressable Market) - with conflicts handled
- SAM (Serviceable Addressable Market)
- SOM (Serviceable Obtainable Market)
- Market insights

### 💼 Business Model
- Business model overview
- Revenue model
- Pricing strategy
- Customer acquisition
- Key partnerships
- Distribution strategy

### 👥 Team
- Complete team list from both sources
- Roles and backgrounds
- Source attribution for each member

### 💰 Financial Data & Traction
- Funding raised (all rounds)
- Currently seeking funding
- Revenue (conflicts handled if different between sources)
- Traction metrics
- Financial projections

### 🏆 Competitive Landscape
- All competitors mentioned in either source
- Similarities and differences
- Source attribution

### 🛡️ Competitive Advantages & IP
- Patents (granted and pending)
- Proprietary technology
- Network effects
- Other competitive advantages

### 🔧 Technology
- Technical approach and details

### 🚀 Go-to-Market Strategy
- GTM strategy and execution plans

### 🏅 Awards & Recognition
- Awards, grants, and recognition

### 💬 Customer Evidence & Validation
- Customer testimonials
- Case studies
- Validation evidence

### 💡 Additional Insights
- Any other relevant information

### 📝 Analysis Notes
- Notes about pitch deck completeness
- Quality assessment

## Source Attribution

Every piece of information is clearly marked with its source:

- `*(pitch deck)* ` - Information from the pitch deck analysis
- `*(web analysis)* ` - Information from the web scraping and analysis
- `*(pitch deck & web analysis)* ` - Information found in both sources

## Handling Conflicts

When the pitch deck and web analysis provide different information for the same field (e.g., different market sizes), the merged analysis shows both:

```markdown
**Total Addressable Market (TAM):**
- **Pitch Deck**: $6.2B by 2036
- **Web Analysis**: $1.5B - $3B annually
- *Note: Different timeframes and calculation methods*
```

## Missing Information

If information is not available from either source, it's clearly marked as:

```markdown
*Information not found*
```

## Pipeline Architecture

1. **Load Analyses** - Reads `deck_analysis.md` and `web_analysis.md` from the company folder
2. **Merge with LLM** - Uses GPT-4o to intelligently merge information, handle conflicts, and structure data
3. **Render** - Formats the structured data into comprehensive markdown

## Integration with Main Pipeline

The merge analysis is automatically run as the third step in the main pipeline:

```bash
python -m src.main
```

This will:
1. Run web analysis (if URL provided)
2. Run deck analysis (if PDF found)
3. Run merge analysis (if either analysis completed)

Output structure:
```
output/
  company-name/
    web_analysis.md      # Web scraping results
    deck_analysis.md     # Pitch deck analysis
    merged_analysis.md   # Comprehensive overview ⭐
```

## Requirements

- OpenAI API key set in `.env` file or `OPENAI_API_KEY` environment variable
- Both deck and web analysis pipelines should be run first (or at least one of them)

## Example

```bash
# Run all three pipelines on companies in pitches.csv
python -m src.main

# Or run merge analysis separately on existing analyses
python -m src.merge_analysis.main
```
