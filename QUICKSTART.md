# Quick Start Guide

## Running the Complete Analysis

Follow these steps to analyze all your companies with both web and deck analysis:

### Step 1: Prepare Your CSV File

Edit `input/pitches.csv` with your companies:

```csv
startup_name,startup_url
Chartera,https://www.chartera.io/
Supercity AI,https://www.supercity.ai/
```

### Step 2: Add PDF Files

Place PDF files in `input/decks/` with names matching the company names:

**Naming Convention:**
- Company name → lowercase → spaces/special chars become dashes
- "Chartera" → `chartera.pdf`
- "Supercity AI" → `supercity-ai.pdf`
- "MyStartup Inc." → `mystartup-inc.pdf`

**Example:**
```bash
input/decks/
├── chartera.pdf
├── supercity-ai.pdf
└── another-company.pdf
```

**Helper Tool:**
```bash
# Check which PDFs you need to rename
python scripts/prepare_pdfs.py
```

### Step 3: Run the Analysis

```bash
# Make sure your virtual environment is active
source .venv/bin/activate

# Run the complete analysis
python -m src.main
```

### Step 4: Check Your Results

```bash
# Results will be organized by company
output/
├── chartera/
│   ├── web_analysis.md      # Website analysis
│   └── deck_analysis.md     # Pitch deck analysis
└── supercity-ai/
    ├── web_analysis.md
    └── deck_analysis.md
```

## What Happens

For each company in your CSV:

1. ✅ Creates a folder: `output/{company-slug}/`
2. 🌐 Analyzes the website → `web_analysis.md`
3. 📊 Finds matching PDF → `deck_analysis.md`
4. 📁 Both files saved in the company folder

## Common Scenarios

### Company has URL but no PDF
- ✅ Web analysis runs
- ⚠️ Deck analysis skipped
- Result: Only `web_analysis.md` created

### Company has PDF but no URL
- ⚠️ Web analysis skipped  
- ✅ Deck analysis runs
- Result: Only `deck_analysis.md` created

### Company has both
- ✅ Web analysis runs
- ✅ Deck analysis runs
- Result: Both files created

## Troubleshooting

### "No PDF found for Company X"

**Problem:** PDF filename doesn't match the company name

**Solution:** Rename the PDF to match the slug format:
```bash
cd input/decks
mv "Current Name.pdf" "company-name.pdf"
```

**Example:**
```bash
# For "Supercity AI" in CSV
mv "Supercity Deck.pdf" "supercity-ai.pdf"
```

### "Web analysis failed"

**Possible causes:**
- URL is not accessible
- Website blocks scraping
- OpenAI API issue

**Solution:**
- Check the URL is correct and accessible
- Review the error message for details
- Deck analysis will still run if PDF exists

### Finding the Right PDF Name

Use the helper script:
```bash
python scripts/prepare_pdfs.py
```

This shows:
- ✅ Companies with matching PDFs
- ❌ Companies missing PDFs
- 💡 Suggested rename commands

## Examples

### Example 1: Two Companies, Both Have Everything

**Input CSV:**
```csv
startup_name,startup_url
Chartera,https://www.chartera.io/
Supercity AI,https://www.supercity.ai/
```

**PDFs:**
```
input/decks/chartera.pdf
input/decks/supercity-ai.pdf
```

**Command:**
```bash
python -m src.main
```

**Output:**
```
output/
├── chartera/
│   ├── web_analysis.md
│   └── deck_analysis.md
└── supercity-ai/
    ├── web_analysis.md
    └── deck_analysis.md
```

### Example 2: Mixed Scenario

**Input CSV:**
```csv
startup_name,startup_url
Chartera,https://www.chartera.io/
LocalBiz,
OnlineCo,https://www.onlineco.com/
```

**PDFs:**
```
input/decks/chartera.pdf
input/decks/localbiz.pdf
```

**Result:**
- **Chartera**: Both analyses (has URL + PDF)
- **LocalBiz**: Only deck analysis (no URL, has PDF)
- **OnlineCo**: Only web analysis (has URL, no PDF)

## Next Steps

After running the analysis:

1. **Review the Results**: Check the markdown files in each company folder
2. **Iterate**: Add more companies to the CSV and run again
3. **Customize**: Modify prompts in `src/web_analysis/prompts/` or `src/deck_analysis/prompts.py`

## Still Have Questions?

- 📖 Full documentation: `MAIN_USAGE.md`
- 🔧 Implementation details: `IMPLEMENTATION_SUMMARY.md`
- 📚 General setup: `README.md`
