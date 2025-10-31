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
