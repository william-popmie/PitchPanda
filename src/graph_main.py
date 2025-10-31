import os
import csv
from typing import Dict, Any

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END

from .prompts import prompt
from .schemas import Analysis
from .utils import fetch_website_text, slugify, ensure_dir
from .renderer import render_markdown

# ---------- Config ----------
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
INPUT_CSV  = os.path.join(os.path.dirname(__file__), "..", "input", "pitches.csv")

# ---------- State ----------
class AnalysisState(BaseModel):
    startup_name: str
    startup_url: str
    website_text: str = ""
    result_json: Dict[str, Any] = {}

# ---------- LLM + Parser ----------
load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
parser = JsonOutputParser()

# ---------- Nodes ----------
def fetch_node(state: AnalysisState) -> AnalysisState:
    state.website_text = fetch_website_text(state.startup_url)
    return state

def analyze_node(state: AnalysisState) -> AnalysisState:
    chain = prompt | llm | parser
    state.result_json = chain.invoke({
        "startup_name": state.startup_name,
        "startup_url": state.startup_url,
        "website_text": state.website_text
    })
    return state

def validate_node(state: AnalysisState) -> AnalysisState:
    """
    Convert raw dict to our Pydantic Analysis model, do minimal corrections.
    Ensures homepage is included in sources.
    """
    # 1) coerce into Analysis (raises ValidationError if malformed)
    try:
        analysis = Analysis(**state.result_json)
    except ValidationError as e:
        # If the model returned malformed JSON, try a minimal fallback shape.
        # (Keeps pipeline from crashing; you can harden this later.)
        minimal = {
            "problem": {"general": "Unknown", "example": "Unknown"},
            "solution": {"what_it_is": "Unknown", "how_it_works": "Unknown", "example": "Unknown"},
            "product_type": "Unknown",
            "sector": "Unknown",
            "subsector": "Unknown",
            "sources": [state.startup_url]
        }
        analysis = Analysis(**minimal)

    # 2) Ensure homepage is in sources (dedupe)
    srcs = list(dict.fromkeys(list(analysis.sources or []) + [state.startup_url]))
    analysis.sources = srcs

    # 3) Write back to state as dict
    state.result_json = analysis.model_dump()
    return state

def write_node(state: AnalysisState) -> AnalysisState:
    ensure_dir(OUTPUT_DIR)
    analysis = Analysis(**state.result_json)
    md = render_markdown(state.startup_name, state.startup_url, analysis)
    outpath = os.path.join(OUTPUT_DIR, f"{slugify(state.startup_name)}.md")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ Wrote {outpath}")
    return state

# ---------- Build Graph ----------
def build_graph():
    builder = StateGraph(AnalysisState)
    builder.add_node("fetch", fetch_node)
    builder.add_node("analyze", analyze_node)
    builder.add_node("validate", validate_node)
    builder.add_node("write", write_node)
    builder.set_entry_point("fetch")
    builder.add_edge("fetch", "analyze")
    builder.add_edge("analyze", "validate")
    builder.add_edge("validate", "write")
    builder.add_edge("write", END)
    return builder.compile()

graph = build_graph()

# ---------- Runner ----------
def run_csv(csv_path=INPUT_CSV):
    if not os.path.exists(csv_path):
        raise SystemExit(f"Missing input CSV at {csv_path} (expected columns: startup_name,startup_url)")

    # Read with utf-8-sig to strip BOM if present
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # Normalize headers in case of BOM / stray spaces
        if reader.fieldnames:
            reader.fieldnames = [ (fn or "").lstrip("\ufeff").strip() for fn in reader.fieldnames ]

        for row in reader:
            # Normalize keys coming from DictReader just in case
            row = { (k or "").lstrip("\ufeff").strip(): (v or "").strip() for k, v in row.items() }

            name = row.get("startup_name", "")
            url  = row.get("startup_url", "")
            if not name or not url:
                print(f"Skipping row (missing name/url): {row}")
                continue

            state = AnalysisState(startup_name=name, startup_url=url)
            graph.invoke(state)

if __name__ == "__main__":
    run_csv()
