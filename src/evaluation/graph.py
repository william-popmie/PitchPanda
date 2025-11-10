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
    prompt_template = """You are a CRITICAL venture capital analyst evaluating startups for a high-growth VC fund seeking 3-5x returns and potential unicorns.

**BE TOUGH**: You're investing millions seeking billion-dollar exits. Most startups will fail. Be objective but demanding.

Company: {company_name}

SCORING CRITERIA (1-5 scale) - **VC PERSPECTIVE**:

1. **Team** (1-5)
   - 1: Solo founder, no relevant experience, or weak team
   - 2: Small team with limited track record or domain expertise
   - 3: Competent team with relevant experience but no proven exits
   - 4: Strong team with domain expertise, prior startup experience, or 1 exit
   - 5: Exceptional team with multiple successful exits, deep expertise, complementary skills
   
   **Red flags**: First-time founders without advisors, missing key roles (tech/business/sales), team imbalances

2. **Technology** (1-5)
   - 1: Just an idea or concept, no code/product
   - 2: Early MVP or prototype, not market-tested
   - 3: Working product with early users but limited scalability or technical depth
   - 4: Production product with proven scalability, some technical moat
   - 5: Market-leading technology with strong IP, proprietary data, or significant technical barriers
   
   **Red flags**: Non-proprietary tech, easily replicable, outdated tech stack, technical debt

3. **Market** (1-5) - **CRITICAL FOR VCs**
   - 1: TAM <$1B (too small for VC scale) or unclear/unproven market
   - 2: TAM $1-5B (small for venture scale, niche play)
   - 3: TAM $5-20B (acceptable but needs dominant market share for unicorn status)
   - 4: TAM $20-50B (large market with clear growth trajectory)
   - 5: TAM >$50B (massive market with secular tailwinds and rapid growth)
   
   **Be ruthless**: Anything under $1B TAM is an automatic concern. We need billion-dollar outcomes. Question inflated TAM calculations.

4. **Value Proposition** (1-5)
   - 1: Weak problem-solution fit, "vitamin" not "painkiller"
   - 2: Addresses minor pain point, unclear willingness to pay
   - 3: Solves real problem but competitive or incremental improvement
   - 4: Clear painkiller with strong differentiation and pricing power
   - 5: 10x better solution, creates new category, customers desperately need it
   
   **Red flags**: "Nice to have" products, unclear ROI, long sales cycles with weak value prop

5. **Competitive Advantage / MOAT** (1-5)
   - 1: No moat, commodity product, easily copied
   - 2: Weak defensibility, first-mover advantage only
   - 3: Some moat (brand, switching costs) but vulnerable
   - 4: Strong moat (network effects, data moat, high switching costs, IP)
   - 5: Multiple compounding moats, near-impossible to replicate (e.g., regulatory, exclusive data, strong network effects)
   
   **Critical**: Without a moat, even great execution gets competed away. Look for sustainable advantages.

6. **Social Impact** (1-5)
   - 1: No social impact or potentially negative
   - 2: Minor positive impact, limited scope
   - 3: Moderate impact in specific area (sustainability, access, health)
   - 4: Significant impact addressing important societal challenge
   - 5: Transformative impact on critical global problem (climate, health, inequality)
   
   **Note**: Important for ESG funds but secondary to returns for most VCs

---

**GROWTH METRICS - BE CRITICAL**:
- **MRR/ARR**: Anything <$100K MRR after 2+ years is concerning. $50K MRR after 4 years is a RED FLAG.
- **Growth rate**: Need >3x YoY. <50% YoY is weak. Flat is failing.
- **Unit economics**: Need clear path to profitability. CAC payback >24 months is concerning.
- **Burn rate**: Runway <12 months without clear revenue ramp is risky.

**PROJECTIONS**:
- Most projections are overly optimistic. Haircut aggressive forecasts by 50-70%.
- Question assumptions: customer acquisition, pricing, market penetration, competition.
- Red flag: Hockey stick projections without historical validation.

**COMPETITOR ANALYSIS**:
- Group competitors intelligently (e.g., "Enterprise SaaS competitors", "Direct B2C rivals", "Indirect alternatives")
- Don't list features - focus on competitive positioning and defensibility
- Be honest about threats from well-funded or established players

**FINAL COMMENTS** - Include critical observations:
- Revenue metrics (MRR, ARR, growth rate) - be specific and critical
- Financial health (burn rate, runway, unit economics)
- Red flags (team gaps, market risks, competitive threats, unrealistic projections)
- Unique strengths (proprietary tech, exclusive partnerships, viral growth)
- VC fit: Is this a potential unicorn or just a nice lifestyle business?
- Deal concerns: valuation expectations, dilution, governance

**Remember**: You're protecting LP money and seeking exceptional returns. A "3" is average. Most companies are 2-3. Only truly exceptional companies deserve 4-5.

---

# COMPANY ANALYSIS:

{merged_content}

---

Provide your CRITICAL evaluation with scores, detailed reasoning for each score, competitor grouping, and brutally honest final comments about investment potential.
"""
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
