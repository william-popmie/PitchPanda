# Pitch Deck Analysis - Quick Start

## ✅ What's Been Created

A complete modular pitch deck analysis system:

```
src/deck_analysis/
├── __init__.py          # Module initialization
├── main.py             # Runner (analyze PDFs)
├── graph.py            # LangGraph workflow
├── schemas.py          # Data models (DeckAnalysis, SlideInsight)
├── prompts.py          # GPT-4 Vision prompts
├── pdf_utils.py        # PDF → Images conversion
├── renderer.py         # Markdown output
└── README.md           # Module documentation
```

## 🚀 How to Use

### 1. Install Dependencies

```bash
# Install poppler (required for PDF processing)
brew install poppler

# Install Python package
pip install pdf2image

# Or reinstall all requirements
pip install -r requirements.txt
```

### 2. Add Your Pitch Deck

Place PDF files in `input/decks/`:
```bash
cp ~/Downloads/my_pitch.pdf input/decks/
```

### 3. Run Analysis

```bash
# Analyze all PDFs in input/decks/
python -m src.deck_analysis.main

# Or analyze a specific file
python -m src.deck_analysis.main input/decks/my_pitch.pdf
```

### 4. View Results

Check `output/decks/` for markdown analysis files.

## 📊 What It Extracts

- **Problem Statement** - What problem is being solved?
- **Solution Overview** - How does the product solve it?
- **Value Proposition** - What makes it unique?
- **Target Market** - Who are the customers?
- **Business Model** - How do they make money?
- **Traction** - Metrics, users, revenue, growth
- **Team** - Key team members
- **Financials** - Revenue projections
- **The Ask** - Funding amount and use
- **Assessment** - Strengths, weaknesses, missing elements

## 🔧 How It Works

**Workflow:**
```
PDF Upload
    ↓
Convert to Images (one per slide)
    ↓
Encode to Base64
    ↓
GPT-4 Vision Analysis
    ↓
Validate with Pydantic
    ↓
Render to Markdown
    ↓
Save to output/decks/
```

**Technology:**
- `pdf2image` - Converts PDF pages to PNG images
- `GPT-4o` - Vision-enabled model for image analysis
- `LangGraph` - Orchestrates the workflow
- `Pydantic` - Validates and structures the output

## 🎯 Example Output Structure

```markdown
# Pitch Deck Analysis: YourStartup

**Total Slides:** 12

---

## 📊 Core Pitch Elements

### 🔴 Problem Statement
[Extracted problem description]

### 💡 Solution Overview
[Extracted solution description]

...

---

## 🎯 Assessment

### ✅ Strengths
- Strong value proposition
- Clear market opportunity

### ⚠️ Weaknesses
- Missing financial projections
- Team slide unclear

### ❌ Missing Elements
- Competitive landscape
- Go-to-market strategy
```

## 💡 Tips

- **PDF Quality**: Higher resolution PDFs = better analysis
- **Slide Count**: Works best with 10-20 slides (standard deck length)
- **Cost**: Uses GPT-4o Vision API (more expensive than text-only)
- **Modular**: Completely separate from website analysis workflow

## 🔄 Integration with Website Analysis

The two modules are **independent**:

- **Website Analysis** (`src/orchestration/graph_main.py`)
  - Input: `input/pitches.csv` (URLs)
  - Output: `output/*.md`
  - Analyzes public websites

- **Deck Analysis** (`src/deck_analysis/main.py`)
  - Input: `input/decks/*.pdf` (pitch decks)
  - Output: `output/decks/*_analysis.md`
  - Analyzes pitch deck slides

You can run them separately or together as needed!
