# PitchPanda

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
# use default PDF path (./Pitches.pdf)
python3 python-backend/main.py

# specify PDF and output file
python3 python-backend/main.py path/to/input.pdf -o links.txt

# don't try to use pdfplumber even if installed
python3 python-backend/main.py input.pdf --no-pdfplumber
```

Output format (UTF-8):

```
anchor_text
url

anchor_text2
url2

...
```

If the extractor cannot find anchor text it will show `(no anchor text)` for
that link. If you see that frequently, installing `pdfplumber` helps in many
cases, and I can also add heuristics to expand the annotation bbox when
extraction returns nothing.

## Generating `requirements.txt` from your venv

If you'd like a `requirements.txt` that captures the exact versions in your
virtual environment, run:

```bash
# activate your venv first
source .venv/bin/activate

# then export pinned requirements
pip freeze > requirements.txt
```

Commit `requirements.txt` if you want reproducible installs for other
developers or deployment.

## Troubleshooting

- If `python3` can't be found, try `python` depending on your system.
- If imports fail, ensure your venv is activated or install packages globally
	(not recommended).
- For missing anchor text: install `pdfplumber` and re-run the extractor.

If you'd like, I can generate a starter `requirements.txt` with current
recommended versions (e.g. `pypdf==3.20.0`, `pdfplumber==0.7.6`) — tell me
if you'd like me to add that file.
# PitchPanda
