## PitchPanda

A small toolkit for working with pitch PDFs and generating pitch-related artifacts.

This README gives a short overview, a CLI-first setup (so a contributor can copy/paste the commands), and clear run instructions for the project already laid out in `src/`.

## Overview

- Purpose: extract, transform, and scaffold pitch content (PDFs, prompts, and output files) to help rapid pitch generation and iteration.
- Layout: the code lives under `src/`, organized into two main analysis modules with shared utilities.

**Project Structure:**
```
src/
├── main.py           # ⭐ MAIN PIPELINE - Runs all three stages
├── core/             # Shared utilities (slugify, ensure_dir, etc.)
├── web_analysis/     # Stage 1: Website analysis workflow
│   ├── main.py       # Entry point for web analysis
│   ├── graph.py      # LangGraph workflow
│   ├── schemas.py    # Data models
│   ├── renderer.py   # Markdown output
│   ├── utils.py      # Web-specific utilities
│   └── prompts/      # Analysis prompts
├── deck_analysis/    # Stage 2: Pitch deck PDF analysis workflow
│   ├── main.py       # Entry point for deck analysis
│   ├── graph.py      # LangGraph workflow
│   ├── schemas.py    # Data models
│   ├── renderer.py   # Markdown output
│   ├── pdf_utils.py  # PDF processing
│   └── prompts.py    # Analysis prompts
└── merge_analysis/   # Stage 3: Merge web + deck → comprehensive overview
    ├── main.py       # Entry point for merge analysis
    ├── graph.py      # LangGraph merge workflow
    ├── schemas.py    # Merged data models
    └── renderer.py   # Comprehensive markdown output
```

**Three-Stage Pipeline:**
1. **Web Analysis** - Scrapes and analyzes company websites (problem/solution, market, competition)
2. **Deck Analysis** - Analyzes pitch deck PDFs with GPT-4 Vision (metrics, team, financials, IP)
3. **Merge Analysis** ⭐ - Combines both sources into one comprehensive, source-attributed overview

## Quick Setup (one-shot, CLI copy/paste)

These commands assume macOS / zsh. They will:

- clone the repository (SSH or HTTPS)
- create + activate a Python virtual environment in `.venv`
- install dependencies from `requirements.txt`
- create a `.env` file and insert an `OPENAI_API_KEY` placeholder for you to replace

Copy and run the block that matches how you clone (SSH or HTTPS):

```bash
# Clone (choose SSH or HTTPS)
# SSH
git clone git@github.com:william-popmie/PitchPanda.git
# or HTTPS
git clone https://github.com/william-popmie/PitchPanda.git

cd PitchPanda

# Ensure input/ and output/ directories exist (safe to run if they already do)
mkdir -p input output input/decks output/decks

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip and install requirements
pip install --upgrade pip setuptools
pip install -r requirements.txt

# Install system dependency for PDF processing (macOS)
brew install poppler

# Create a .env with a placeholder OPENAI_API_KEY so you just edit the value
cat > .env <<'EOF'
OPENAI_API_KEY="insert here"
EOF

echo "Created .env — open it and replace INSERT HERE with your real API key."
```

Windows (PowerShell) equivalent notes:

```powershell
git clone https://github.com/william-popmie/PitchPanda.git
cd PitchPanda
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools
pip install -r requirements.txt

# Ensure input/ and output/ directories exist (PowerShell)
New-Item -ItemType Directory -Force .\input | Out-Null
New-Item -ItemType Directory -Force .\output | Out-Null

# Create .env (PowerShell)
@"
OPENAI_API_KEY="insert here"
"@ | Out-File -Encoding utf8 .env
```

After creation, open `.env` in a text editor and replace the placeholder with your actual API key (do NOT commit the key).

## Running

From the repository root with the virtualenv active you can run the main entrypoints:

### Complete Analysis (RECOMMENDED)
```bash
# Analyzes all companies from input/pitches.csv
# - Runs web analysis on each company's URL
# - Runs deck analysis on matching PDFs in input/decks/
# - Creates a folder per company in output/ with both analyses
python -m src.main

# Or with a custom CSV path
python -m src.main path/to/your/pitches.csv
```

**Output structure:**
```
output/
├── chartera/
│   ├── web_analysis.md
│   └── deck_analysis.md
└── supercity-ai/
    ├── web_analysis.md
    └── deck_analysis.md
```

See [MAIN_USAGE.md](MAIN_USAGE.md) for detailed documentation.

### Website Analysis Only (from CSV)
```bash
# Analyzes startups from input/pitches.csv
python -m src.web_analysis.main

# Or with a custom CSV path
python -m src.web_analysis.main path/to/your/startups.csv
```

### Pitch Deck Analysis Only (PDF)
```bash
# Analyze a specific pitch deck PDF
python -m src.deck_analysis.main input/decks/your_pitch.pdf

# Or analyze all PDFs in input/decks/
python -m src.deck_analysis.main
```

Notes:
- Using `python -m` runs the `src` package as a module so relative imports in `src/` work cleanly.
- If you prefer direct script runs, ensure your `PYTHONPATH` includes `./src`.

## Example: quick smoke test

### Complete Analysis (Both Web + Deck)
1. Ensure `.venv` is active.
2. Ensure `.env` contains a valid `OPENAI_API_KEY`.
3. Ensure `brew install poppler` is installed (macOS).
4. Add startup URLs to `input/pitches.csv`:
   ```csv
   startup_name,startup_url
   Chartera,https://www.chartera.io/
   Supercity AI,https://www.supercity.ai/
   ```
5. Add matching PDF files to `input/decks/`:
   - `chartera.pdf`
   - `supercity-ai.pdf`
6. Run the complete analysis:
   ```bash
   python -m src.main
   ```
7. Check `output/chartera/` and `output/supercity-ai/` for:
   - `web_analysis.md`
   - `deck_analysis.md`

### Website Analysis Only
1. Ensure `.venv` is active.
2. Ensure `.env` contains a valid `OPENAI_API_KEY`.
3. Add startup URLs to `input/pitches.csv`:
   ```csv
   startup_name,startup_url
   Chartera,https://www.chartera.io/
   ```
4. Run the analysis:
   ```bash
   python -m src.web_analysis.main
   ```
5. Check `output/*.md` for generated analyses.

### Pitch Deck Analysis Only
1. Ensure `.venv` is active and `brew install poppler` is installed.
2. Ensure `.env` contains a valid `OPENAI_API_KEY`.
3. Place your pitch deck PDF in `input/decks/`.
4. Run the analysis:
   ```bash
   python -m src.deck_analysis.main
   ```
5. Check `output/decks/*_analysis.md` for results.

## Project structure (top-level)

```
PitchPanda/
├── README.md
├── requirements.txt
├── .env                    # Your API keys (not committed)
├── input/
│   ├── pitches.csv        # Startup URLs for web analysis
│   └── decks/             # PDF pitch decks
├── output/
│   ├── *.md               # Web analysis results
│   └── decks/             # Deck analysis results
└── src/
    ├── core/              # Shared utilities
    │   ├── __init__.py
    │   └── utils.py
    ├── web_analysis/      # Website analysis module
    │   ├── __init__.py
    │   ├── main.py
    │   ├── graph.py
    │   ├── schemas.py
    │   ├── renderer.py
    │   ├── utils.py
    │   └── prompts/
    │       ├── __init__.py
    │       ├── problem_solution.py
    │       └── competition.py
    └── deck_analysis/     # Pitch deck analysis module
        ├── __init__.py
        ├── main.py
        ├── graph.py
        ├── schemas.py
        ├── renderer.py
        ├── pdf_utils.py
        └── prompts.py
```

## Troubleshooting

- `ModuleNotFoundError` after activating `.venv`:
  - Confirm `which python` points to `.venv/bin/python`.
  - Confirm packages installed: `pip show <package>`.

- OpenAI or API key errors:
  - Confirm `.env` contains `OPENAI_API_KEY` and the process loads it (some projects require `python-dotenv`).
  - You can also export it directly for a single run:

```bash
export OPENAI_API_KEY="sk-..."
python -m src.web_analysis.main
```

- If imports fail because modules are under `src/`, prefer `python -m src.web_analysis.main` or set `PYTHONPATH`:

```bash
export PYTHONPATH="$PWD/src:$PYTHONPATH"
python -m src.web_analysis.main
```

## Contributing

- Open an issue for bugs or feature requests.
- For PRs, keep changes focused and add tests where applicable.

## Further improvements (optional)

- Add a `.env.example` file listing required environment variables without secrets.
- Add `requirements-dev.txt` for developer tooling (linters/tests).
- Add a minimal `dev-README.md` describing editor/IDE setup and common tasks.

---

If you'd like, I can also create a `.env.example` and a short `dev-README.md` in this repo—tell me which and I'll add them.
## PitchPanda

Small utilities for working with pitch PDFs.

This README explains, step-by-step, how to install and run the project from
scratch (clone -> venv -> install -> .env -> run), how to manage dependencies
(`pip freeze`), and other useful tips for development on macOS/Linux (zsh) and
Windows.

> Note: The repository contains a `src/` directory. Some run instructions
> below explain how to run code that lives under `src/` (PYTHONPATH or
> `python -m` usage).

## Quickstart (the shortest path)

1. Clone the repo:

```bash
# SSH
git clone git@github.com:william-popmie/PitchPanda.git

# or HTTPS
git clone https://github.com/william-popmie/PitchPanda.git

cd PitchPanda
```

2. Create and activate a virtual environment (macOS / Linux / zsh):

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

4. Create your `.env` (if the project uses secrets / API keys):

```bash
cp .env.example .env   # if .env.example exists
# then edit .env with your values
```

5. Run the project (example):

```bash
python main.py
# or explicitly use the venv python
.venv/bin/python main.py
```

If your code lives under `src/` (module layout), you may need to either set
`PYTHONPATH` or run as a module (see "Running code in `src/`" section).

---

## Detailed instructions and explanation

### 1) Cloning and branches

- Clone as shown above. If the repo uses branches, checkout the branch you
	want:

```bash
git checkout william/langgraph-test
```

### 2) Python versions and `pyenv`

- Recommended Python versions: 3.10 — 3.13.
- If you need multiple Python versions, `pyenv` is a convenient manager.
	Example:

```bash
pyenv install 3.11.6
pyenv local 3.11.6
```

### 3) Virtual environment best practices

- Use a per-project virtualenv: `.venv/` is conventional and already
	included in `.gitignore`.
- Always activate the venv before installing or running code.

Checks to confirm you are using the venv:

```bash
which python   # should point into .venv/bin/python
python --version
pip --version  # shows which python pip belongs to
```

### 4) Installing dependencies

- Prefer installing from `requirements.txt` for reproducible installs:

```bash
pip install -r requirements.txt
```

- If you get `ModuleNotFoundError` for a package (for example `prompts`):

```bash
pip show prompts || pip install prompts
```

- If you are developing and need an editable install for a local package,
	use `pip install -e .` (if `setup.py` / `pyproject.toml` exists) or
	install packages one-by-one during development.

### 5) .env and secrets

- Keep secrets out of git. Use a `.env` file and ensure it's in
	`.gitignore` (this repo already ignores `.env`).
- Create `.env.example` (without secrets) and commit that so other devs know
	which variables to set.

Example `.env.example` (create this file):

```
# copy to .env and fill values
OPENAI_API_KEY=
OTHER_SERVICE_KEY=
```

Loading `.env` values in Python:

- Recommended: install `python-dotenv` and call `load_dotenv()` early in the
	program.

- Alternative: export environment variables in your shell before running:

```bash
export OPENAI_API_KEY="sk-..."
python main.py
```

You can use `direnv` to automatically load `.env` when you cd into the repo.

### 6) Running code in `src/`

This repository uses a `src/` layout. You may need one of the following to
run code cleanly:

- Run as a module (recommended when using `src/`):

```bash
# from repo root
python -m src.main
# or for graph_main
python -m src.graph_main
```

- Set `PYTHONPATH` so imports from `src` resolve:

```bash
export PYTHONPATH="$PWD/src:$PYTHONPATH"
python main.py
```

If imports fail because Python can't find local modules, try running with
`-m` or setting `PYTHONPATH` as above.

### 7) When and how to run `pip freeze > requirements.txt`

- Run `pip freeze > requirements.txt` after you have installed or upgraded
	the packages required by the project and verified the project runs.
- Typical workflow:

```bash
# install a new dependency
pip install somepackage

# run tests / manual checks

# freeze current venv packages to requirements.txt
pip freeze > requirements.txt

# commit
git add requirements.txt
git commit -m "update requirements"
```

Notes:
- `pip freeze` pins exact versions (good for reproducible installs).
- If you have dev-only packages installed, consider creating
	`requirements-dev.txt` or removing dev packages before freezing.
- For a curated approach, use `pip-tools` (`pip-compile`) to manage
	top-level deps and generate a lock file.

### 8) Git: stop tracking files that should be ignored

If you accidentally committed `.venv/`, `input/`, `output/` or similar, run:

```bash
# stop tracking locally but keep files on disk
git rm -r --cached .venv
git rm -r --cached input
git rm -r --cached output
git commit -m "Stop tracking local venv and generated data"
```

If sensitive data was committed you must rotate secrets and consider using
`git filter-repo` to scrub history (this rewrites history—ask if you need
help).

### 9) Troubleshooting common issues

- ModuleNotFoundError even after venv activation
	- Confirm `which python` and `pip --version` show the `.venv` paths.
	- Confirm the package is installed in that venv: `pip show <package>`.

- `python: can't open file 'main'` or similar
	- You ran `python main` instead of `python main.py` or you're in the
		wrong working directory. Use `python main.py` from the repo root or
		specify the full path.

- Imports failing because modules are in `src/`
	- Use `python -m src.main` or set `PYTHONPATH` to include `./src`.

### 10) Recommended developer workflow

1. Create and activate `.venv`.
2. Install `requirements.txt`.
3. Add new dependency via `pip install` while venv is active.
4. Run tests / smoke tests.
5. Freeze: `pip freeze > requirements.txt` if you want to pin exact
	 environment versions.
6. Commit code and `requirements.txt`.

### 11) Optional: create helpful helper files

I can create these for you on request:

- `.env.example` — lists environment variables needed (no secrets).
- `requirements-dev.txt` — dev-only packages (linters, test runners).
- `dev-README.md` — short editor/IDE setup notes (VS Code interpreter
	configuration, launch tasks).

---

If you'd like, I will:

- Add a `.env.example` file populated with likely keys (OPENAI_API_KEY, ...)
- Create a pinned `requirements.txt` from my environment (or run it in your
	venv if you want exact local pins)
- Add a short `dev-README.md` describing how to configure VS Code to use
	`.venv`

Tell me which of those you'd like and I'll add them.

Small utilities for working with pitch PDFs.

## Requirements

 - Python 3.8+ (3.10 or newer recommended)
 - A POSIX-like shell (instructions use zsh/bash)

This project uses `pypdf` to read annotations and optionally `pdfplumber` to
extract visible text inside annotation rectangles. If `pdfplumber` is not
installed the script will still extract URIs but may not find anchor text
located in small annotation areas.

## Create and activate a virtual environment (recommended)

From the repository root (macOS / Linux, zsh):

```bash
# create a venv in .venv
python3 -m venv .venv

# activate it
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Install dependencies

If there's a `requirements.txt` in the repo you can install with:

```bash
pip install -r requirements.txt
```

Notes:
- `pypdf` is used to read PDF pages and annotations.
- `pdfplumber` is optional but improves anchor text extraction by reading
	the exact rectangular area of an annotation.

## Running the extractor

There is a script at `python-backend/main.py` which extracts anchor text and
the associated URL from a PDF and writes them to a UTF-8 text file.

Usage examples:

```bash
# PitchPanda

Small utilities for working with pitch PDFs.

This README documents everything you need to reinstall, set up a local
development environment, add secrets safely, run the project, and update
dependencies (including when to run `pip freeze > requirements.txt`). The
instructions below target macOS with `zsh` but will work on most Linux
distributions with small adjustments. Windows notes are included where
relevant.

## Table of contents

- Prerequisites
- Create and activate a virtual environment
- Install dependencies
- .env / secrets management
- Running the project
- Updating dependencies and `requirements.txt`
- Git: stop tracking files already committed
- Troubleshooting
- Recommended workflows and best practices

## Prerequisites

- Python: 3.10 — 3.13 recommended (the repo has been used with 3.11+ and
	3.13 on macOS). Check your local version:

```bash
python --version
```

- Git installed and a working clone of this repo.
- A POSIX-like shell (zsh/bash). Windows users: use PowerShell or WSL.

If you need a specific Python install manager consider `pyenv` (helps
managing multiple Python versions) or use the system Python if you prefer.

## Create and activate a virtual environment (recommended)

Always create a virtual environment for this project so packages are
isolated and `pip freeze` captures only the project dependencies.

From the repository root (macOS / Linux, zsh):

```bash
# create a venv in .venv using the default `python` on your PATH
python -m venv .venv

# activate it (zsh/bash)
source .venv/bin/activate

# confirm you're using the virtualenv's python
which python
python --version
pip --version   # shows pip and the path it belongs to
```

On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Notes:
- If `python` resolves to a system Python you don't want, use the explicit
	path to the Python binary you want (for example `python3.11` or the
	`pyenv`-managed shim).
- We put virtualenv in `.venv/` by convention; that directory is already
	included in `.gitignore`.

## Install dependencies

Install from the project `requirements.txt` (recommended) while the virtual
environment is active:

```bash
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

If a package is missing (for example `ModuleNotFoundError: No module named
'prompts'`), check:

1. That your virtualenv is activated.
2. `pip show prompts` to verify whether `prompts` is installed in the venv.
3. `pip install prompts` to add it locally, then re-run your script.

If you are developing and frequently change packages, you may prefer to
install editable dependencies or use a tool like `pip-tools` / `poetry` for
locking. This repository currently expects a `requirements.txt` file for
reproducible installs.

## .env / secrets management

Some projects require API keys or other secrets. For local development use a
`.env` file placed in the repository root (it is already ignored in
`.gitignore`). Do NOT commit this file.

Create a `.env.example` containing the variable names (no secrets) and add
instructions for obtaining keys. Example `.env.example`:

```text
# copy this to .env and fill values
OPENAI_API_KEY=
OTHER_SERVICE_KEY=
```

Create your `.env` by copying the example and filling values:

```bash
cp .env.example .env
# then edit .env with your editor
```

How to load `.env` values in Python:

- Option A (recommended): use `python-dotenv` and call `load_dotenv()` from
	your app (requires adding `python-dotenv` to `requirements.txt`).
- Option B: export the variables manually in your shell before running the
	project:

```bash
export OPENAI_API_KEY="sk-..."
python main.py
```

Keep secrets out of git. If you accidentally committed a secret, rotate the
secret at the provider (e.g., generate a new API key) and remove the secret
from the repo history if needed.

## Running the project

With the venv activated you can run the main script from the repo root. Use
the venv python explicitly if you're unsure:

```bash
# with venv activated
python main.py

# or explicitly use the virtualenv python
.venv/bin/python main.py
```

If you see ImportError / ModuleNotFoundError:

```bash
# quick checks
python -c "import sys; print(sys.executable); print(sys.path)"
pip show prompts || echo "prompts not installed in this environment"
```

If you installed a package but still see an import error, check that the
`pip` you used belongs to the same Python executable you are running:

```bash
# pip should point into .venv
pip --version
# this should print the pip path inside .venv
```

## Updating dependencies and `requirements.txt`

When to run `pip freeze > requirements.txt`:

- After you have installed or upgraded packages for the project and tested
	that everything works, create a new `requirements.txt` to capture exact
	versions for reproducibility.
- Example workflow when you add a dependency:

```bash
# activate venv
source .venv/bin/activate

# install the new dependency (example)
pip install somepackage

# run the project / tests, verify it works

# then update requirements.txt (pins exact versions)
pip freeze > requirements.txt

# commit the changes
git add requirements.txt
git commit -m "Add somepackage and update requirements"
```

Notes on best practice:
- `pip freeze` will list all packages installed in your environment. If you
	have extra dev-only packages installed and you don't want them in
	`requirements.txt`, either uninstall them before freezing or maintain
	separate files like `requirements-dev.txt`.
- If you want curated (minimal) requirements instead of full environment
	pins, use `pip-compile` from `pip-tools` to generate a locked file.

## Git: stop tracking files already committed

If you added `.venv/`, `input/`, or other generated files to git before
adding them to `.gitignore`, you must remove them from the index so git
stops tracking them (this does NOT delete the files locally):

```bash
# example: stop tracking .venv and input/ and output/
git rm -r --cached .venv
git rm -r --cached input
git rm -r --cached output
git commit -m "Stop tracking local venv and generated data; update .gitignore"
```

If you need to purge sensitive files from history, that's a larger and more
dangerous operation (use `git filter-repo` or `git filter-branch`). If you
need help with that I can outline safe steps.

## Troubleshooting (common cases)

- ModuleNotFoundError after activating venv

	- Confirm the venv is active: `which python` should point into `.venv/`
	- Confirm the package is installed in that venv: `pip show <package>`
	- If not installed, `pip install <package>` while venv is active.

- `python: can't open file 'main': [Errno 2] No such file or directory`

	- You tried `python main` instead of `python main.py` or running from the
		wrong working directory. Use `python main.py` from the repo root or
		provide the full path.

- I changed code and it's not picked up when I run the script

	- Make sure you're running the script with the same python interpreter
		(the one from `.venv`). If using an editor/IDE, configure it to use
		`.venv`'s interpreter.

## Recommended workflow / checklist before committing

1. Activate `.venv`.
2. Run unit tests (if any) and smoke tests.
3. If you added/changed dependencies, run `pip freeze > requirements.txt`.
4. Ensure you haven't accidentally committed secrets (`git status`) and
	 that `.env` remains untracked.
5. If you removed large files from tracking, run the git untrack commands
	 shown above and commit.

## Advanced / optional tools

- `pyenv` to manage Python versions.
- `pip-tools` (`pip-compile`) to manage pinned dependencies and separate
	top-level vs transitive pins.
- `direnv` to automatically load `.env` into your shell.

---

If you want, I can:

- Create a `.env.example` file in the repo with the common keys you need to
	fill in.
- Add a `requirements.txt` generated from my environment as a starting point.
- Add a short `dev-README.md` with one-line editor/IDE setup instructions
	(VS Code settings for using `.venv`, etc.).

Tell me which of those you'd like me to add and I'll update the repo.
