"""LangGraph workflow for web analysis."""

import os
from typing import Dict, Any

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END

from .prompts import prompt, COMP_PROMPT
from .utils import fetch_website_text
from .schemas import Analysis, Competitor


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
    """Fetch website text content."""
    state.website_text = fetch_website_text(state.startup_url)
    return state


def analyze_node(state: AnalysisState) -> AnalysisState:
    """Analyze website and extract problem/solution."""
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
    """Build and compile the LangGraph workflow."""
    builder = StateGraph(AnalysisState)
    builder.add_node("fetch", fetch_node)
    builder.add_node("analyze", analyze_node)
    builder.add_node("validate", validate_node)
    builder.add_node("competition", competition_node)
    
    builder.set_entry_point("fetch")
    builder.add_edge("fetch", "analyze")
    builder.add_edge("analyze", "validate")
    builder.add_edge("validate", "competition")
    builder.add_edge("competition", END)
    
    return builder.compile()


# Build the graph
analysis_graph = build_graph()
