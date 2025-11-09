# PitchPanda Main Orchestrator

## Overview

The main entry point (`src/main.py`) orchestrates both web analysis and pitch deck analysis for each company listed in `input/pitches.csv`.

## Features

- **Automated Analysis**: Runs both web and deck analysis for each company
- **Organized Output**: Creates a folder per company in the `output/` directory
- **Flexible Matching**: Intelligently finds PDF files matching company names
- **Robust Error Handling**: Continues processing even if one analysis fails

## Setup

### 1. Input CSV Format

The `input/pitches.csv` file should have the following columns:

```csv
startup_name,startup_url
Chartera,https://www.chartera.io/
Supercity AI,https://www.supercity.ai/
```

### 2. PDF Naming Convention

Place PDF files in `input/decks/` with names matching the company names:

- `chartera.pdf` for "Chartera"
- `supercity-ai.pdf` for "Supercity AI"

The system uses flexible matching:
- Exact slug match (e.g., `chartera.pdf`)
- Case-insensitive match
- Partial match (company name in filename)

## Usage

### Run All Companies

```bash
python -m src.main
```

### Use Custom CSV

```bash
python -m src.main path/to/custom_pitches.csv
```

## Output Structure

After running, you'll have the following structure:

```
output/
├── chartera/
│   ├── web_analysis.md
│   └── deck_analysis.md
└── supercity-ai/
    ├── web_analysis.md
    └── deck_analysis.md
```

## What It Does

For each company in the CSV:

1. **Creates Company Folder**: `output/{company-slug}/`
2. **Web Analysis**: 
   - Fetches website content
   - Analyzes problem/solution
   - Identifies competitors
   - Saves to `web_analysis.md`
3. **Deck Analysis**:
   - Finds matching PDF in `input/decks/`
   - Converts to images
   - Analyzes with GPT-4 Vision
   - Saves to `deck_analysis.md`

## Error Handling

- If no URL is provided, web analysis is skipped
- If no PDF is found, deck analysis is skipped
- Individual failures don't stop the batch process
- Detailed error messages are printed for debugging

## Example Output

```
============================================================
🚀 PitchPanda - Complete Startup Analysis
============================================================
📄 Reading from: /path/to/pitches.csv
📁 Output to: /path/to/output
============================================================

============================================================
📊 Analyzing: Chartera
============================================================
  🌐 Running web analysis...
  ✅ Web analysis saved to: /path/to/output/chartera/web_analysis.md
  🎯 Running deck analysis on: chartera.pdf
  ✅ Deck analysis saved to: /path/to/output/chartera/deck_analysis.md

  📁 Results saved to: /path/to/output/chartera
     ✓ web_analysis.md
     ✓ deck_analysis.md

============================================================
✅ Analysis complete!
📊 Processed 2 companies
📁 Results in: /path/to/output
============================================================
```

## Individual Module Usage

You can still run individual analyses if needed:

### Web Analysis Only
```bash
python -m src.web_analysis.main
```

### Deck Analysis Only
```bash
python -m src.deck_analysis.main input/decks/company.pdf
```

## Requirements

- Python 3.10+
- OpenAI API key in `.env`
- All dependencies from `requirements.txt`

## Troubleshooting

### "No PDF found for {company}"
- Check that the PDF filename matches the company name (slugified)
- Verify the file is in `input/decks/` directory
- Check file extension is `.pdf` (lowercase)

### "Web analysis failed"
- Verify the URL is accessible
- Check OpenAI API key is set
- Review the detailed error traceback

### "Deck analysis failed"
- Ensure PDF is valid and not corrupted
- Check that you have GPT-4 Vision API access
- Verify sufficient API credits
