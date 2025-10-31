import os, csv
from dotenv import load_dotenv
from typing import Dict, Any
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END

from prompts import prompt
from utils import fetch_website_text, slugify

load_dotenv()
print("[debug] Current working directory:", os.getcwd())
# Print whether API key(s) are present (don't print the key itself)
has_pitch_key = bool(os.getenv("PITCH_PANDA_API_KEY"))
has_openai_key = bool(os.getenv("OPENAI_API_KEY"))
print(f"[debug] PITCH_PANDA_API_KEY present: {has_pitch_key} | OPENAI_API_KEY present: {has_openai_key}")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

class AnalysisState(BaseModel):
    startup_name: str
    startup_url: str
    website_text: str = ""
    result_json: Dict[str, Any] = {}

parser = JsonOutputParser()

def fetch_node(state: AnalysisState) -> AnalysisState:
    print(f"[debug][fetch] start fetching for: {state.startup_url}")
    state.website_text = fetch_website_text(state.startup_url)
    print(f"[debug][fetch] fetched {len(state.website_text or '')} chars for {state.startup_name}")
    return state

def analyze_node(state: AnalysisState) -> AnalysisState:
    print(f"[debug][analyze] starting analysis for: {state.startup_name}")
    chain = prompt | llm | parser
    state.result_json = chain.invoke({"website_text": state.website_text})
    print(f"[debug][analyze] analysis complete for: {state.startup_name} (keys: {len(state.result_json.keys()) if isinstance(state.result_json, dict) else 'unknown'})")
    return state

def write_node(state: AnalysisState) -> AnalysisState:
    # Simple writer: you can reuse the render_markdown from Option A
    from main import Analysis, render_markdown  # reuse schema & renderer
    a = Analysis(**state.result_json)
    md = render_markdown(state.startup_name, state.startup_url, a)
    os.makedirs("output", exist_ok=True)
    out = os.path.join("output", f"{slugify(state.startup_name)}.md")
    print(f"[debug][write] writing output to: {out}")
    with open(out, "w", encoding="utf-8") as f:
        f.write(md)
    return state

# Build graph
builder = StateGraph(AnalysisState)
builder.add_node("fetch", fetch_node)
builder.add_node("analyze", analyze_node)
builder.add_node("write", write_node)
builder.set_entry_point("fetch")
builder.add_edge("fetch", "analyze")
builder.add_edge("analyze", "write")
builder.add_edge("write", END)
graph = builder.compile()

def run_csv(csv_path="input/pitches.csv"):
    print(f"[debug] run_csv starting with path: {csv_path}")
    if not os.path.exists(csv_path):
        print(f"[debug] CSV not found: {csv_path}")
        return

    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            state = AnalysisState(
                startup_name=row["startup_name"].strip(),
                startup_url=row["startup_url"].strip(),
            )
            print(f"[debug] invoking graph for: {state.startup_name} ({state.startup_url})")
            try:
                graph.invoke(state)
                print(f"✅ {row['startup_name']} done")
            except Exception as e:
                print(f"[error] failed processing {state.startup_name}: {e}")
                # continue to next row

if __name__ == "__main__":
    run_csv()
