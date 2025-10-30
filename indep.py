# simple_evaluator.py
"""
Very simple startup evaluator.
Reads all markdown files from input/results/
Outputs analysis markdowns to output/analysis/
"""

import os
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
try:
    from utils import slugify
except Exception:
    def slugify(text: str) -> str:
        return ''.join(c.lower() if c.isalnum() else '-' for c in text).strip('-')

# Load API key
load_dotenv()
API_KEY = os.getenv("PITCH_PANDA_API_KEY") or os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("PITCH_PANDA_API_KEY or OPENAI_API_KEY not set.")
os.environ["OPENAI_API_KEY"] = API_KEY

# --- folders ---
# Read inputs from input/summaries/*.md
INPUT_DIR = Path("input/summaries")
# Write outputs to output/analysis/
OUTPUT_DIR = Path("output/analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- model ---
model = ChatOpenAI(model_name="gpt-5", temperature=0)

# --- evaluation prompt ---
PROMPT = """You are a professional venture capital analyst. Read the provided company report carefully and rate the startup objectively on multiple independent dimensions.

Each criterion must be evaluated independently (do NOT let one influence another).

### Criteria
- Team (1=solo/inexperienced, 5=experienced team)
- Technology (1=idea, 5=market-ready)
- Market (1=very small, 5=very large)
- Value Proposition (1=unclear, 5=strong fit)
- Competitive Advantage (1=easily copied, 5=highly defensible)
- Socially Impactful (1=none, 5=highly transformative)

### Output Format
Return your answer in this exact Markdown format:

# [Company Name] Evaluation

**Team:** [1–5] — [short reason]  
**Technology:** [1–5] — [short reason]  
**Market:** [1–5] — [short reason]  
**Value Proposition:** [1–5] — [short reason]  
**Competitive Advantage:** [1–5] — [short reason]  
**Socially Impactful:** [1–5] — [short reason]

---

### Competitors
[List competitors and note if any are highly similar.]

---

### Comments
[3–6 sentences. Balanced opinion on whether to investigate further, with reasoning.]
"""

# --- main loop ---
def main():
    files = sorted(INPUT_DIR.glob("*.md"))
    if not files:
        print(f"No markdown files found in {INPUT_DIR}/")
        return

    total = len(files)
    pad = max(2, len(str(total)))

    for i, f in enumerate(files, start=1):
        print(f"→ Evaluating {f.name} ({i}/{total}) ...")
        text = f.read_text(encoding="utf-8")

        message = HumanMessage(
            content=f"""Below is a company report. Evaluate it using the instructions provided.

{PROMPT}

[BEGIN REPORT]
{text}
[END REPORT]
"""
        )

        response = model.invoke([message])
        result = response.content

        # Create a slug from the filename or first header
        company_slug = f.stem
        lines = text.splitlines()
        if lines and lines[0].strip().startswith('#'):
            # use header as company name if present
            company_name = lines[0].lstrip('#').strip()
            company_slug = slugify(company_name)
        else:
            company_slug = slugify(company_slug)

        out_name = f"analysis-{i:0{pad}d}-{company_slug}.md"
        out_path = OUTPUT_DIR / out_name
        out_path.write_text(result, encoding="utf-8")

        print(f"✓ Saved to {out_path}")

if __name__ == "__main__":
    main()
