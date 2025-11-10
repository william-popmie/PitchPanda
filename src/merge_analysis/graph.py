"""
LangGraph pipeline for merging deck and web analysis.
"""
import os
from typing import TypedDict, Optional
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from .schemas import MergedAnalysis

# Load environment variables
load_dotenv()


class MergeState(TypedDict):
    """State for the merge pipeline."""
    company_name: str
    deck_analysis_path: Optional[str]
    web_analysis_path: Optional[str]
    deck_content: Optional[str]
    web_content: Optional[str]
    merged_analysis: Optional[dict]


def load_analyses(state: MergeState) -> MergeState:
    """Load deck and web analysis content from files."""
    print("  📖 Loading analysis files...")
    
    deck_content = None
    web_content = None
    
    # Load deck analysis if available
    if state.get("deck_analysis_path") and os.path.exists(state["deck_analysis_path"]):
        with open(state["deck_analysis_path"], "r", encoding="utf-8") as f:
            deck_content = f.read()
        print(f"    ✓ Loaded deck analysis ({len(deck_content)} chars)")
    else:
        print("    ⚠️  No deck analysis found")
    
    # Load web analysis if available
    if state.get("web_analysis_path") and os.path.exists(state["web_analysis_path"]):
        with open(state["web_analysis_path"], "r", encoding="utf-8") as f:
            web_content = f.read()
        print(f"    ✓ Loaded web analysis ({len(web_content)} chars)")
    else:
        print("    ⚠️  No web analysis found")
    
    return {
        **state,
        "deck_content": deck_content,
        "web_content": web_content,
    }


def merge_analyses(state: MergeState) -> MergeState:
    """Merge deck and web analyses using LLM."""
    print("  🔄 Merging analyses with LLM...")
    
    # Initialize LLM with structured output
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    structured_llm = llm.with_structured_output(MergedAnalysis)
    
    # Build the prompt based on what's available
    deck_content = state.get("deck_content")
    web_content = state.get("web_content")
    company_name = state.get("company_name", "Unknown")
    
    if not deck_content and not web_content:
        raise ValueError("No analysis content available to merge")
    
    # Create prompt template
    prompt_template = """You are an expert analyst tasked with creating a comprehensive company overview by merging information from two sources:
1. Pitch deck analysis (if available)
2. Web analysis (if available)

Company: {company_name}

{deck_section}

{web_section}

Your task is to create a comprehensive merged analysis that:

1. **Combines all available information** - Include everything relevant from both sources
2. **Attributes sources clearly** - Use source field to indicate "pitch deck", "web analysis", or "both"
3. **Handles conflicts** - When information conflicts between sources, use ConflictingInfo to show both versions
4. **Marks missing information** - If information is not available from either source, leave it as None/null
5. **Preserves details** - Don't summarize away important details; keep specifics like numbers, names, dates

Guidelines:
- For SourcedInfo fields: set source to "pitch deck", "web analysis", or "both" depending on where the info came from
- For ConflictingInfo: use when pitch deck and web have different values (e.g., different market sizes)
- For team members: include everyone mentioned in either source
- For competitors: merge lists from both sources
- For metrics: preserve both current state and projections
- **For Problem/Solution**: Extract web analysis problem/solution/examples separately from pitch deck details
  - problem_web: General problem from web analysis
  - problem_example_web: Example scenario from web analysis
  - problem_deck: More specific problem details from pitch deck
  - solution_web: Product/solution description from web analysis
  - solution_example_web: Example usage from web analysis
  - solution_deck: More detailed solution information from pitch deck
- Be thorough - this is the definitive overview of the company

Extract and structure all available information into the MergedAnalysis schema."""

    # Build deck section
    deck_section = ""
    if deck_content:
        deck_section = f"""
# PITCH DECK ANALYSIS:
```
{deck_content}
```
"""
    else:
        deck_section = "\n# PITCH DECK ANALYSIS: Not available\n"
    
    # Build web section
    web_section = ""
    if web_content:
        web_section = f"""
# WEB ANALYSIS:
```
{web_content}
```
"""
    else:
        web_section = "\n# WEB ANALYSIS: Not available\n"
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | structured_llm
    
    # Invoke the chain
    result = chain.invoke({
        "company_name": company_name,
        "deck_section": deck_section,
        "web_section": web_section,
    })
    
    print("    ✓ Merge complete")
    
    return {
        **state,
        "merged_analysis": result.model_dump(),
    }


# Build the graph
def build_merge_graph():
    """Build the LangGraph for merging analyses."""
    workflow = StateGraph(MergeState)
    
    # Add nodes
    workflow.add_node("load_analyses", load_analyses)
    workflow.add_node("merge_analyses", merge_analyses)
    
    # Define edges
    workflow.set_entry_point("load_analyses")
    workflow.add_edge("load_analyses", "merge_analyses")
    workflow.add_edge("merge_analyses", END)
    
    return workflow.compile()


# Create the graph instance
merge_graph = build_merge_graph()
