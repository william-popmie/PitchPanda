# PitchPanda Architecture & Workflow

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PitchPanda System                         │
└─────────────────────────────────────────────────────────────────┘

INPUT FILES
┌─────────────────────┐         s┌─────────────────────┐
│  pitches.csv        │         │   input/decks/      │
│                     │         │                     │
│  startup_name       │         │  chartera.pdf       │
│  startup_url        │         │  supercity-ai.pdf   │
└─────────────────────┘         └─────────────────────┘
         │                                │
         └────────────┬───────────────────┘
                      ▼
         ┌────────────────────────┐
         │    src/main.py         │
         │  (Main Orchestrator)   │
         └────────────────────────┘
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐
│ Web Analysis     │      │ Deck Analysis    │
│ Module           │      │ Module           │
└──────────────────┘      └──────────────────┘
         │                         │
         └────────────┬────────────┘
                      ▼
         ┌────────────────────────┐
         │   output/{company}/    │
         │                        │
         │  web_analysis.md       │
         │  deck_analysis.md      │
         └────────────────────────┘
```

## Main Orchestrator Workflow

```
START
  │
  ├─► Read pitches.csv
  │    └─► Parse company names & URLs
  │
  ├─► For each company:
  │    │
  │    ├─► Create output folder: output/{company-slug}/
  │    │
  │    ├─► WEB ANALYSIS
  │    │    ├─► Check if URL exists
  │    │    ├─► Run web_analysis.graph
  │    │    │    ├─► Fetch website content
  │    │    │    ├─► Analyze with GPT-4
  │    │    │    ├─► Extract problem/solution
  │    │    │    ├─► Find competitors
  │    │    │    └─► Validate results
  │    │    └─► Save web_analysis.md
  │    │
  │    ├─► DECK ANALYSIS
  │    │    ├─► Find matching PDF
  │    │    ├─► Run deck_analysis.graph
  │    │    │    ├─► Convert PDF to images
  │    │    │    ├─► Encode images to base64
  │    │    │    ├─► Analyze with GPT-4 Vision
  │    │    │    └─► Validate results
  │    │    └─► Save deck_analysis.md
  │    │
  │    └─► Continue to next company
  │
  └─► Print summary
       └─► END
```

## Web Analysis Module

```
┌─────────────────────────────────────────────────────────────────┐
│                      Web Analysis Graph                          │
└─────────────────────────────────────────────────────────────────┘

Input: {startup_name, startup_url}
  │
  ├─► [FETCH NODE]
  │    └─► Fetch website HTML/text content
  │
  ├─► [ANALYZE NODE]
  │    └─► GPT-4 extracts:
  │         • Problem (general + example)
  │         • Solution (what + how + example)
  │         • Product type
  │         • Sector/Subsector
  │         • Active locations
  │         • Sources
  │
  ├─► [VALIDATE NODE]
  │    └─► Validate Pydantic models
  │         Ensure data completeness
  │
  ├─► [COMPETITION NODE]
  │    └─► GPT-4 identifies competitors:
  │         • Name, website, location
  │         • Problem similarity
  │         • Solution differences
  │         • Similarities
  │
  ├─► [WRITE NODE]
  │    └─► Render markdown
  │         Save to output/
  │
Output: Markdown analysis file
```

## Deck Analysis Module

```
┌─────────────────────────────────────────────────────────────────┐
│                      Deck Analysis Graph                         │
└─────────────────────────────────────────────────────────────────┘

Input: {pdf_path}
  │
  ├─► [CONVERT PDF NODE]
  │    └─► pdf2image converts PDF → PNG images
  │         One image per slide
  │
  ├─► [ENCODE IMAGES NODE]
  │    └─► Encode each image to base64
  │
  ├─► [ANALYZE DECK NODE]
  │    └─► GPT-4 Vision analyzes all slides:
  │         • Problem statement
  │         • Solution description
  │         • Market metrics
  │         • Team composition
  │         • Competition mentioned
  │         • Business model
  │         • Observations & claims
  │         • Missing/present elements
  │
  ├─► [VALIDATE NODE]
  │    └─► Validate Pydantic models
  │         Ensure schema compliance
  │
Output: Markdown analysis file
```

## Data Flow

```
CSV Record
    ↓
┌─────────────────────┐
│ Company: Chartera   │
│ URL: chartera.io    │
└─────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Find PDF: input/decks/chartera.pdf      │
└─────────────────────────────────────────┘
    ↓
┌──────────────────┐     ┌──────────────────┐
│ Web Analysis     │     │ Deck Analysis    │
│ LangGraph Flow   │     │ LangGraph Flow   │
└──────────────────┘     └──────────────────┘
    ↓                            ↓
┌──────────────────┐     ┌──────────────────┐
│ Analysis Object  │     │ DeckAnalysis     │
│ (Pydantic)       │     │ Object           │
└──────────────────┘     └──────────────────┘
    ↓                            ↓
┌──────────────────┐     ┌──────────────────┐
│ Markdown         │     │ Markdown         │
│ Renderer         │     │ Renderer         │
└──────────────────┘     └──────────────────┘
    ↓                            ↓
┌──────────────────────────────────────────┐
│   output/chartera/                       │
│   ├── web_analysis.md                    │
│   └── deck_analysis.md                   │
└──────────────────────────────────────────┘
```

## File Organization

```
PitchPanda/
│
├── input/
│   ├── pitches.csv              # Company list
│   └── decks/                   # PDF storage
│       ├── chartera.pdf
│       └── supercity-ai.pdf
│
├── output/                      # Generated analyses
│   ├── chartera/
│   │   ├── web_analysis.md
│   │   └── deck_analysis.md
│   └── supercity-ai/
│       ├── web_analysis.md
│       └── deck_analysis.md
│
├── src/
│   ├── main.py                  # 🎯 Main orchestrator
│   ├── core/                    # Shared utilities
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── web_analysis/            # Web analysis module
│   │   ├── main.py             # Standalone entry
│   │   ├── graph.py            # LangGraph workflow
│   │   ├── schemas.py          # Pydantic models
│   │   ├── renderer.py         # MD generation
│   │   ├── utils.py            # Scraping
│   │   └── prompts/            # LLM prompts
│   └── deck_analysis/           # Deck analysis module
│       ├── main.py             # Standalone entry
│       ├── graph.py            # LangGraph workflow
│       ├── schemas.py          # Pydantic models
│       ├── renderer_updated.py # MD generation
│       ├── pdf_utils.py        # PDF → images
│       └── prompts.py          # LLM prompts
│
├── scripts/
│   └── prepare_pdfs.py          # PDF naming helper
│
└── Documentation
    ├── README.md                # Main documentation
    ├── QUICKSTART.md            # Quick start guide
    ├── MAIN_USAGE.md            # Detailed usage
    └── IMPLEMENTATION_SUMMARY.md # Technical details
```

## Key Components

### 1. Main Orchestrator (`src/main.py`)
- **Purpose**: Coordinate both analyses for all companies
- **Responsibilities**:
  - CSV parsing
  - PDF matching
  - Error handling
  - Output organization

### 2. Web Analysis Module
- **Technology**: LangGraph + GPT-4
- **Input**: Company URL
- **Output**: Problem/solution analysis, competitors
- **Key Features**:
  - Website scraping
  - Structured data extraction
  - Competitor research

### 3. Deck Analysis Module
- **Technology**: LangGraph + GPT-4 Vision
- **Input**: PDF file
- **Output**: Comprehensive deck analysis
- **Key Features**:
  - PDF to image conversion
  - Visual analysis
  - Metric extraction
  - Team analysis

## Technology Stack

```
┌─────────────────────────────────────────┐
│           Application Layer              │
│  • Python 3.10+                         │
│  • LangGraph (orchestration)            │
│  • LangChain (LLM integration)          │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│              AI Layer                    │
│  • OpenAI GPT-4 (text analysis)         │
│  • OpenAI GPT-4 Vision (image analysis) │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│           Data Layer                     │
│  • Pydantic (validation)                │
│  • CSV (input data)                     │
│  • Markdown (output format)             │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│          Utilities                       │
│  • pdf2image (PDF processing)           │
│  • Poppler (PDF backend)                │
│  • BeautifulSoup (web scraping)         │
└─────────────────────────────────────────┘
```

## Error Handling Strategy

```
┌─────────────────────────┐
│   Company Processing    │
└─────────────────────────┘
          │
          ├─► Web Analysis
          │   ├─► Success → Save file
          │   └─► Failure → Log error, continue
          │
          ├─► Deck Analysis
          │   ├─► Success → Save file
          │   └─► Failure → Log error, continue
          │
          └─► Next Company
```

**Philosophy**: Fail gracefully, continue processing
- Individual failures don't stop the batch
- Detailed error messages for debugging
- Partial results are still saved
