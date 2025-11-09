# Pitch Deck Analysis Module

This module analyzes pitch deck PDFs using GPT-4 Vision to extract key information.

## Structure

```
src/deck_analysis/
├── __init__.py
├── main.py           # Main runner
├── graph.py          # LangGraph workflow
├── schemas.py        # Pydantic models
├── prompts.py        # GPT-4 Vision prompts
├── pdf_utils.py      # PDF to image conversion
└── renderer.py       # Markdown output renderer
```

## Features

- **PDF Conversion**: Converts pitch deck PDFs to images
- **Vision Analysis**: Uses GPT-4 Vision to analyze slides
- **Structured Output**: Extracts:
  - Problem statement
  - Solution overview
  - Value proposition
  - Target market
  - Business model
  - Traction metrics
  - Team information
  - Financials
  - Funding ask
  - Strengths/weaknesses assessment

## Setup

1. Install system dependency (macOS):
```bash
brew install poppler
```

2. Install Python packages:
```bash
pip install -r requirements.txt
```

3. Ensure `OPENAI_API_KEY` is in your `.env` file

## Usage

### Analyze a specific deck:
```bash
python -m src.deck_analysis.main input/decks/my_pitch.pdf
```

### Analyze all decks in input/decks/:
```bash
python -m src.deck_analysis.main
```

## Output

Analysis results are saved to `output/decks/` as markdown files.

## Workflow

1. **Convert PDF** → Images (one per slide)
2. **Encode Images** → Base64 for API
3. **Analyze Deck** → GPT-4 Vision extracts insights
4. **Validate** → Structure data with Pydantic
5. **Render** → Save as formatted markdown
