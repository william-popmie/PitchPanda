"""
LangGraph pipeline for company evaluation and scoring.
"""
import os
from typing import TypedDict, Optional
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from .schemas import CompanyEvaluation

# Load environment variables
load_dotenv()


class EvaluationState(TypedDict):
    """State for the evaluation pipeline."""
    company_name: str
    merged_analysis_path: Optional[str]
    merged_content: Optional[str]
    evaluation: Optional[dict]


def load_merged_analysis(state: EvaluationState) -> dict:
    """Load merged analysis content from file."""
    print("  📖 Loading merged analysis...")
    
    merged_content = None
    
    if state.get("merged_analysis_path") and os.path.exists(state["merged_analysis_path"]):
        with open(state["merged_analysis_path"], "r", encoding="utf-8") as f:
            merged_content = f.read()
        print(f"    ✓ Loaded merged analysis ({len(merged_content)} chars)")
    else:
        print("    ⚠️  No merged analysis found")
    
    return {"merged_content": merged_content}


def evaluate_company(state: EvaluationState) -> dict:
    """Evaluate company with LLM scoring."""
    print("  📊 Evaluating company...")
    
    # Initialize LLM with structured output
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    structured_llm = llm.with_structured_output(CompanyEvaluation)
    
    company_name = state.get("company_name", "Unknown")
    merged_content = state.get("merged_content")
    
    if not merged_content:
        raise ValueError("No merged analysis content available to evaluate")
    
    # Create evaluation prompt
    prompt_template = """You are a venture capital analyst evaluating a startup for potential investment.

Based on the comprehensive company analysis below, evaluate this company on 6 criteria using a 1-5 scale.

Company: {company_name}

SCORING CRITERIA (1-5 scale):

1. **Team** (1-5)
   - 1: Lone founder with limited relevant experience
   - 2: Small team or founder with some relevant experience
   - 3: Team with decent experience, may have gaps
   - 4: Strong team with relevant expertise and prior success
   - 5: Exceptional team with multiple successful exits, deep domain expertise

2. **Technology** (1-5)
   - 1: Just an idea, no product development yet
   - 2: Early prototype or MVP stage
   - 3: Working product with some users/customers
   - 4: Product in market with proven traction
   - 5: Market-ready scalable product with strong technical moat

3. **Market** (1-5)
   - 1: Very small or unclear market (<$100M TAM)
   - 2: Small market ($100M-$500M TAM)
   - 3: Medium market ($500M-$2B TAM)
   - 4: Large market ($2B-$10B TAM)
   - 5: Very large market (>$10B TAM) with strong growth

4. **Value Proposition** (1-5)
   - 1: Solution doesn't clearly address the problem
   - 2: Addresses problem but weak fit or unclear differentiation
   - 3: Good problem-solution fit, some differentiation
   - 4: Strong problem-solution fit with clear differentiation
   - 5: Perfect problem-solution fit, unique and compelling value

5. **Competitive Advantage / MOAT** (1-5)
   - 1: No defensibility, easy to replicate
   - 2: Weak moat, some barriers but easily overcome
   - 3: Moderate moat (brand, network effects starting)
   - 4: Strong moat (IP, exclusive partnerships, significant network effects)
   - 5: Very strong moat (multiple defensibility layers, hard to replicate)

6. **Social Impact** (1-5)
   - 1: No meaningful social impact
   - 2: Minor positive impact in limited scope
   - 3: Moderate positive impact in specific domain
   - 4: Significant positive impact, addresses important challenge
   - 5: Transformative impact, solves critical societal problem

COMPETITOR ANALYSIS:
- Group competitors by similar characteristics (e.g., "CBD-based therapeutics", "Enterprise SaaS platforms", "Direct competitors")
- Don't repeat similar text for each competitor - group them intelligently
- Focus on what makes each group similar/different

FINAL COMMENTS:
Include interesting observations about:
- MRR, ARR, or revenue metrics (growth rate, sustainability)
- Financial projections (realistic? aggressive? concerns?)
- Unique aspects or red flags
- Anything unusual, particularly positive, or concerning
- Risk factors or opportunities

---

# COMPANY ANALYSIS:

{merged_content}

---

Provide your evaluation with scores, reasoning, competitor grouping, and final comments."""

    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | structured_llm
    
    # Invoke the chain
    result = chain.invoke({
        "company_name": company_name,
        "merged_content": merged_content,
    })
    
    print("    ✓ Evaluation complete")
    
    return {"evaluation": result.model_dump()}


# Build the graph
def build_evaluation_graph():
    """Build the LangGraph for evaluation."""
    workflow = StateGraph(EvaluationState)
    
    # Add nodes
    workflow.add_node("load_analysis", load_merged_analysis)
    workflow.add_node("evaluate", evaluate_company)
    
    # Define edges
    workflow.set_entry_point("load_analysis")
    workflow.add_edge("load_analysis", "evaluate")
    workflow.add_edge("evaluate", END)
    
    return workflow.compile()


# Create the graph instance
evaluation_graph = build_evaluation_graph()
