# PitchPanda

PitchPanda is an AI-powered analysis pipeline for VC analysts to evaluate startup pitch decks and websites. It takes a CSV list of startups and pitch deck PDFs as input, then outputs markdown analyses per startup with important metrics, market insights, and competitive positioning.

## How it works

**Three-stage pipeline:**
1. **Web Analysis** — Scrapes and analyzes company websites (problem/solution, market, competition)
2. **Deck Analysis** — Extracts key data from pitch PDFs using GPT-4 Vision (metrics, team, financials)
3. **Merge Analysis** — Combines both sources into one comprehensive overview with source attribution

## Tech stack & output

Built with **LangGraph** for orchestration, **GPT-4 Vision** for visual PDF analysis, and **LLM-powered reasoning** for web content interpretation. Each analysis stage uses structured schemas (Pydantic models) to ensure consistent output formatting.

**Output format:** Markdown files with source attribution (e.g., `web_analysis.md` and `deck_analysis.md` per company, plus a merged comprehensive analysis). Analyses include structured sections for market opportunity, competitive landscape, team composition, financials, and key differentiators—all extracted and synthesized from raw sources.

## Quick start

```bash
git clone https://github.com/william-popmie/PitchPanda.git
cd PitchPanda

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
brew install poppler  # macOS only

# Set your OpenAI API key
export OPENAI_API_KEY="sk-..."

# Run analysis on all startups
python -m src.main
```

Results appear in `output/` organized by startup name.

## Key components

- **`web_analysis/`** — Website scraping & LLM-based competitive analysis
- **`deck_analysis/`** — PDF parsing & vision-based deck interpretation  
- **`evaluation/`** — Structured assessment workflows
- **`merge_analysis/`** — Combines insights and generates final reports
