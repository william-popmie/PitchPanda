# Main Orchestrator Implementation Summary

## What Was Added

### 1. Main Orchestrator (`src/main.py`)
A new main entry point that coordinates both web and deck analysis for all companies in the CSV file.

**Key Features:**
- Reads companies from `input/pitches.csv`
- Runs web analysis on each company URL
- Automatically finds matching PDF files in `input/decks/`
- Creates organized output with one folder per company
- Handles errors gracefully - continues processing even if one analysis fails

**Output Structure:**
```
output/
├── company-name-1/
│   ├── web_analysis.md
│   └── deck_analysis.md
└── company-name-2/
    ├── web_analysis.md
    └── deck_analysis.md
```

### 2. PDF Matching Logic
The system intelligently finds PDF files matching company names using:
- Exact slug match (e.g., `chartera.pdf` for "Chartera")
- Case-insensitive matching
- Partial matching (company name within filename)

### 3. Documentation

**MAIN_USAGE.md**: Comprehensive guide covering:
- Setup instructions
- Usage examples
- Output structure
- Error handling
- Troubleshooting tips

**Updated README.md**:
- Added "Complete Analysis" as the recommended workflow
- Updated examples to show the new main orchestrator
- Maintained backwards compatibility with individual modules

### 4. Helper Script (`scripts/prepare_pdfs.py`)
Utility to help rename PDF files to match company names from CSV:
- Lists all companies and their expected PDF filenames
- Shows existing PDFs
- Suggests rename commands for matches

## How to Use

### Basic Usage
```bash
# Run complete analysis on all companies
python -m src.main
```

### With Custom CSV
```bash
python -m src.main path/to/custom.csv
```

### Individual Modules (Still Available)
```bash
# Web analysis only
python -m src.web_analysis.main

# Deck analysis only
python -m src.deck_analysis.main input/decks/company.pdf
```

## What Stayed the Same

- Individual modules (`web_analysis`, `deck_analysis`) work exactly as before
- All existing functionality is preserved
- No breaking changes to existing code
- Original output formats unchanged

## Migration Guide

### Before (Two Separate Commands)
```bash
# Step 1: Run web analysis
python -m src.web_analysis.main

# Step 2: Run deck analysis
python -m src.deck_analysis.main

# Result: Scattered output files
output/
├── chartera.md            # web analysis
├── supercity-ai.md        # web analysis
└── decks/
    ├── chartera_analysis.md    # deck analysis
    └── supercity-ai_analysis.md
```

### After (One Command)
```bash
# Single command runs both
python -m src.main

# Result: Organized by company
output/
├── chartera/
│   ├── web_analysis.md
│   └── deck_analysis.md
└── supercity-ai/
    ├── web_analysis.md
    └── deck_analysis.md
```

## Requirements

### Input Files
1. **CSV File** (`input/pitches.csv`):
   ```csv
   startup_name,startup_url
   Chartera,https://www.chartera.io/
   Supercity AI,https://www.supercity.ai/
   ```

2. **PDF Files** (`input/decks/`):
   - `chartera.pdf`
   - `supercity-ai.pdf`

### Environment
- Python 3.10+
- OpenAI API key in `.env`
- All dependencies from `requirements.txt`
- Poppler installed (for PDF processing)

## Error Handling

The orchestrator is robust:
- **Missing URL**: Skips web analysis, continues with deck
- **Missing PDF**: Skips deck analysis, continues with web
- **Analysis Failure**: Logs error, continues with next company
- **Invalid CSV**: Clear error message with expected format

## Benefits

1. **Convenience**: One command to run everything
2. **Organization**: Clean folder structure per company
3. **Flexibility**: Still supports individual module execution
4. **Robustness**: Graceful error handling and recovery
5. **Scalability**: Processes any number of companies efficiently

## Testing

To test the implementation:

1. Ensure you have at least one company in `input/pitches.csv`
2. Place a matching PDF in `input/decks/`
3. Run: `python -m src.main`
4. Check `output/{company-name}/` for both analysis files

## Future Enhancements

Potential improvements for later:
- Parallel processing for faster batch analysis
- Progress bar for large batches
- Summary report across all companies
- Export to different formats (JSON, HTML)
- Comparison analysis across companies
