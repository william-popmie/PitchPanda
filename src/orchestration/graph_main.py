import os
import csv
from typing import Dict, Any

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END

from ..prompts.prompts_problem_solution import prompt
from ..core.utils import fetch_website_text, slugify, ensure_dir
from ..core.renderer import render_markdown
from ..prompts.prompts_competition import COMP_PROMPT
from ..core.schemas import Analysis, Competitor


# ---------- Config ----------
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "output"))
INPUT_CSV  = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "input", "pitches.csv"))

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
    Ensures homepage is included in sources and active_locations is a list.
    """
    try:
        analysis = Analysis(**state.result_json)
    except ValidationError:
        minimal = {
            "problem": {"general": "Unknown", "example": "Unknown"},
            "solution": {"what_it_is": "Unknown", "how_it_works": "Unknown", "example": "Unknown"},
            "product_type": "Unknown",
            "sector": "Unknown",
            "subsector": "Unknown",
            "active_locations": [],   
            "sources": [state.startup_url]
        }
        analysis = Analysis(**minimal)

    # Ensure homepage is in sources (dedupe)
    srcs = list(dict.fromkeys(list(analysis.sources or []) + [state.startup_url]))
    analysis.sources = srcs

    # Ensure active_locations is a list (and clean strings)
    if not isinstance(analysis.active_locations, list):
        analysis.active_locations = []
    analysis.active_locations = [str(x).strip() for x in analysis.active_locations if str(x).strip()]

    state.result_json = analysis.model_dump()
    return state


def write_node(state: AnalysisState) -> AnalysisState:
    ensure_dir(OUTPUT_DIR)
    analysis = Analysis(**state.result_json)
    md = render_markdown(state.startup_name, state.startup_url, analysis)
    outpath = os.path.join(OUTPUT_DIR, f"{slugify(state.startup_name)}.md")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Wrote {outpath}")
    return state

def competition_node(state: AnalysisState) -> AnalysisState:
    """Use the validated Analysis (problem/solution/etc.) to propose competitors."""
    chain = COMP_PROMPT | llm | parser

    a = Analysis(**state.result_json)
    payload = {
        "startup_name": state.startup_name,
        "startup_url": state.startup_url,
        "problem_general": a.problem.general,
        "problem_example": a.problem.example,
        "solution_what": a.solution.what_it_is,
        "solution_how": a.solution.how_it_works,
        "solution_example": a.solution.example,
        "product_type": a.product_type,
        "sector": a.sector,
        "subsector": a.subsector,
        "active_locations": ", ".join(a.active_locations) if a.active_locations else "[]",
    }

    raw = chain.invoke(payload)
    # raw should be {"competition": [ ... ]}; be defensive
    comp_list = raw.get("competition", []) if isinstance(raw, dict) else []
    # Coerce each item via pydantic (drops bad fields, ensures lists exist)
    clean_comp = []
    for item in comp_list:
        try:
            clean_comp.append(Competitor(**item).model_dump())
        except Exception:
            continue

    # Write back into the Analysis blob -> state
    a.competition = [Competitor(**c) for c in clean_comp]
    state.result_json = a.model_dump()
    return state


# ---------- Build Graph ----------
def build_graph():
    builder = StateGraph(AnalysisState)
    builder.add_node("fetch", fetch_node)
    builder.add_node("analyze", analyze_node)
    builder.add_node("validate", validate_node)

    # NEW
    builder.add_node("competition", competition_node)

    builder.add_node("write", write_node)
    builder.set_entry_point("fetch")
    builder.add_edge("fetch", "analyze")
    builder.add_edge("analyze", "validate")

    # NEW edge
    builder.add_edge("validate", "competition")

    builder.add_edge("competition", "write")
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
