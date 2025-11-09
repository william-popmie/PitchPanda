# PitchPanda Project Reorganization Summary

## Overview
The project has been reorganized to provide a clear separation between the two main analysis workflows:
- **Web Analysis**: Analyzes startup websites
- **Deck Analysis**: Analyzes pitch deck PDFs

## New Structure

```
src/
├── core/                      # Shared utilities only
│   ├── __init__.py
│   └── utils.py              # slugify, ensure_dir
│
├── web_analysis/             # Website analysis workflow (NEW)
│   ├── __init__.py
│   ├── main.py              # Entry point (replaces orchestration/graph_main.py)
│   ├── graph.py             # LangGraph workflow
│   ├── schemas.py           # Problem, Solution, Analysis, Competitor (moved from core)
│   ├── renderer.py          # Markdown rendering (moved from core)
│   ├── utils.py             # fetch_website_text, etc. (moved from core)
│   └── prompts/             # Analysis prompts (moved from src/prompts/)
│       ├── __init__.py
│       ├── problem_solution.py
│       └── competition.py
│
└── deck_analysis/            # Pitch deck analysis workflow (existing, improved)
    ├── __init__.py          # Enhanced with exports
    ├── main.py
    ├── graph.py
    ├── schemas.py
    ├── renderer.py
    ├── renderer_updated.py
    ├── pdf_utils.py
    └── prompts.py
```

## What Changed

### Files Moved

#### From `src/orchestration/` → `src/web_analysis/`
- `graph_main.py` → `main.py` (refactored to be cleaner)
- Workflow extracted to `graph.py`

#### From `src/prompts/` → `src/web_analysis/prompts/`
- `prompts_problem_solution.py` → `problem_solution.py`
- `prompts_competition.py` → `competition.py`

#### From `src/core/` → `src/web_analysis/`
- `schemas.py` (web-specific schemas: Problem, Solution, Analysis, Competitor)
- `renderer.py` (web-specific markdown rendering)
- Web utilities extracted to `web_analysis/utils.py`

### Files Updated

#### `src/core/utils.py`
- Now contains only shared utilities: `slugify`, `ensure_dir`
- Web-specific utilities moved to `web_analysis/utils.py`

#### `src/core/__init__.py`
- Updated to export only shared utilities

#### `src/web_analysis/__init__.py`
- Created with proper exports for the module

#### `src/deck_analysis/__init__.py`
- Enhanced with proper exports

#### `README.md`
- Updated project structure diagram
- Updated run commands:
  - OLD: `python -m src.orchestration.graph_main`
  - NEW: `python -m src.web_analysis.main`
- Updated examples and documentation

### Files Created

#### `src/web_analysis/main.py`
- New entry point for web analysis
- Cleaner interface than old graph_main.py
- Better error messages and progress reporting

#### `src/web_analysis/graph.py`
- LangGraph workflow separated from main
- Cleaner organization

#### `src/web_analysis/utils.py`
- Web-specific utilities:
  - `fetch_website_text()`
  - `ensure_scheme()`
  - `hostname()`

#### `src/web_analysis/schemas.py`
- Web analysis data models
- Independent from deck analysis schemas

#### `src/web_analysis/renderer.py`
- Markdown rendering for web analysis
- Independent from deck analysis rendering

### Directories to Remove (Old)

These directories can now be safely removed:
- `src/orchestration/` (functionality moved to web_analysis)
- `src/prompts/` (moved to web_analysis/prompts)

## How to Use

### Web Analysis (Website Analysis)
```bash
# Analyze startups from input/pitches.csv
python -m src.web_analysis.main

# Or with custom CSV
python -m src.web_analysis.main path/to/startups.csv
```

### Deck Analysis (PDF Analysis)
```bash
# Analyze a specific pitch deck
python -m src.deck_analysis.main input/decks/my_pitch.pdf

# Or analyze all PDFs in input/decks/
python -m src.deck_analysis.main
```

## Benefits of New Structure

1. **Clear Separation**: Web analysis and deck analysis are now completely independent modules
2. **Consistent Organization**: Both modules follow the same pattern (main.py, graph.py, schemas.py, etc.)
3. **Better Imports**: No more confusion about where files come from
4. **Easier Maintenance**: Changes to one workflow don't affect the other
5. **Cleaner Core**: Core module only contains truly shared utilities
6. **Scalability**: Easy to add new analysis workflows in the future

## Migration Notes

If you have any custom scripts or code that imports from the old structure, update them as follows:

```python
# OLD imports
from src.orchestration.graph_main import run_csv, graph
from src.core.schemas import Analysis, Competitor
from src.core.renderer import render_markdown
from src.core.utils import fetch_website_text
from src.prompts.prompts_problem_solution import prompt

# NEW imports
from src.web_analysis.main import run_csv
from src.web_analysis.graph import analysis_graph
from src.web_analysis.schemas import Analysis, Competitor
from src.web_analysis.renderer import render_markdown
from src.web_analysis.utils import fetch_website_text
from src.web_analysis.prompts import prompt
```

## Backward Compatibility Note

The old command paths will no longer work:
- ❌ `python -m src.orchestration.graph_main`
- ✅ `python -m src.web_analysis.main`

Update any scripts, CI/CD pipelines, or documentation that reference the old paths.
