"""
Prompts for GPT-4 Vision analysis of pitch deck slides.
"""
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage


SLIDE_ANALYSIS_PROMPT = """You are analyzing a pitch deck slide. Extract key information from this slide.

For this slide, identify:
1. The slide title or main topic
2. Key points or takeaways (bullet points)
3. Any visual elements (charts, graphs, images, diagrams)

Return your analysis in JSON format:
{
    "slide_title": "Title of the slide",
    "key_points": ["point 1", "point 2", ...],
    "visual_elements": "Description of charts/images if any"
}

Be concise and focus on the most important information."""


DECK_SUMMARY_PROMPT = """You are analyzing a complete pitch deck. Your role is to extract ALL METRICS AND NUMBERS with appropriate confidence levels.

CRITICAL RULES:
1. EXTRACT ALL NUMBERS - even if labels are vague or missing
2. Mark confidence level for each metric:
   - "high" = Explicitly labeled (e.g., "Seed Funding: $2M", "MRR: $50K")
   - "medium" = Inferred from context but reasonable (e.g., "$2M raised" → likely funding)
   - "low" = Vague or unclear (e.g., "significant revenue" with a number nearby)
3. Add notes when something seems unrealistic, uncertain, or needs clarification
4. Distinguish between current facts and projections
5. GO INTO DETAIL - don't stay high level (e.g., separate seed/series A/B/C, TAM/SAM/SOM)
6. Present competition AS SHOWN in deck - note that this may be biased
7. DO NOT be persuasive - be factual and neutral

CONFIDENCE LEVELS:

**High Confidence** (explicitly labeled):
- "Seed Funding: $1.5M" ✅
- "MRR: $25K" ✅
- "TAM: $10B" ✅
- "Churn Rate: 2%" ✅

**Medium Confidence** (inferred but reasonable):
- "Raised $1.5M in 2024" → Infer as funding, note stage uncertain
- "$25K monthly revenue" → Likely MRR, but not explicitly stated
- "10B market" → Likely TAM, but TAM/SAM/SOM unclear

**Low Confidence** (vague, needs context):
- "Significant traction" with nearby numbers
- Unlabeled chart axes
- Unclear timeframes

METRICS TO EXTRACT (capture ALL, mark confidence):

**Funding (go into detail):**
- Seed Funding, Pre-Seed, Series A/B/C/D
- Bridge Round, Convertible Note
- Total Raised, Current Round Target
- Valuation, Pre-Money, Post-Money
- Runway (months), Burn Rate
- Investor names/firms if mentioned

**Traction Metrics:**
- MRR, ARR
- Total Revenue, Revenue Last Month/Quarter/Year
- Users (total, active, MAU, DAU)
- Paying Customers, Free Users
- Growth Rate (MoM, QoQ, YoY)
- Retention Rate, Engagement metrics

**LOIs (Letters of Intent):**
- Number of LOIs
- Total LOI Value
- Individual LOI values
- Contract timeline

**Market Size (go into detail):**
- TAM (Total Addressable Market)
- SAM (Serviceable Addressable Market)
- SOM (Serviceable Obtainable Market)
- Year-over-year market growth rate
- Geographic breakdown if mentioned

**Financial Metrics:**
- Current Revenue, Projected Revenue
- Gross Margin, Net Margin, Profit Margin
- Burn Rate, Monthly/Quarterly Burn
- Unit Economics: LTV, CAC, LTV/CAC ratio
- Payback Period
- Churn Rate, Monthly/Annual Churn
- EBITDA, Cash Flow
- Run Rate

**Product/Usage Metrics:**
- Conversion Rate
- Time to Value
- NPS (Net Promoter Score)
- Active Usage metrics

**Team:**
- Names, Roles (CEO, CTO, COO, CFO, etc.)
- Previous Experience (be specific: "Ex-Google Engineer", "Former Founder of X (acquired by Y)")
- Years of experience in industry
- Notable exits, IPOs

**Competition:**
- Competitors mentioned
- Market positioning claims

EXTRACTION FORMAT:

Return JSON in this exact structure:
{
    "problem_statement": "Brief factual description of problem",
    "solution_overview": "Brief factual description of solution",
    "value_proposition": "Value prop as stated",
    "target_market": "Target market as described",
    "business_model": "How they make money",
    
    "metrics": {
        "funding": [
            {
                "label": "Seed Funding",
                "value": "$1.5M",
                "context": "Raised in Q1 2024 from Acme Ventures",
                "is_projection": false,
                "confidence": "high",
                "notes": null
            },
            {
                "label": "Series A Target",
                "value": "$5M",
                "context": "Seeking to raise",
                "is_projection": true,
                "confidence": "high",
                "notes": null
            },
            {
                "label": "Funding (stage uncertain)",
                "value": "$2M",
                "context": "Mentioned without specifying round",
                "is_projection": false,
                "confidence": "medium",
                "notes": "Stage not explicitly labeled"
            }
        ],
        "traction": [
            {
                "label": "MRR",
                "value": "$50K",
                "context": "As of October 2025",
                "is_projection": false,
                "confidence": "high",
                "notes": null
            },
            {
                "label": "Monthly Revenue",
                "value": "$30K",
                "context": "From slide 8",
                "is_projection": false,
                "confidence": "medium",
                "notes": "Not explicitly labeled as MRR, but appears to be recurring"
            },
            {
                "label": "Active Users",
                "value": "10,000",
                "context": null,
                "is_projection": false,
                "confidence": "high",
                "notes": null
            },
            {
                "label": "MoM Growth",
                "value": "15%",
                "context": "Last 6 months average",
                "is_projection": false,
                "confidence": "high",
                "notes": null
            },
            {
                "label": "Projected Users",
                "value": "100,000",
                "context": "By end of 2026",
                "is_projection": true,
                "confidence": "high",
                "notes": "Seems ambitious given current growth rate"
            }
        ],
        "market_size": [
            {
                "label": "TAM",
                "value": "$5B",
                "context": "Global market for X",
                "is_projection": false,
                "confidence": "high",
                "notes": null
            },
            {
                "label": "SAM",
                "value": "$500M",
                "context": "US market",
                "is_projection": false,
                "confidence": "high",
                "notes": null
            },
            {
                "label": "Market Size (TAM/SAM unclear)",
                "value": "$2B",
                "context": "Mentioned on slide 5",
                "is_projection": false,
                "confidence": "medium",
                "notes": "Not specified if TAM or SAM"
            }
        ],
        "financials": [
            {
                "label": "Gross Margin",
                "value": "80%",
                "context": null,
                "is_projection": false,
                "confidence": "high",
                "notes": null
            },
            {
                "label": "ARR Projection",
                "value": "$1M",
                "context": "By EOY 2025",
                "is_projection": true,
                "confidence": "high",
                "notes": null
            },
            {
                "label": "LTV",
                "value": "$5,000",
                "context": null,
                "is_projection": false,
                "confidence": "high",
                "notes": null
            },
            {
                "label": "CAC",
                "value": "$500",
                "context": null,
                "is_projection": false,
                "confidence": "high",
                "notes": null
            },
            {
                "label": "Churn Rate",
                "value": "2%",
                "context": "Monthly",
                "is_projection": false,
                "confidence": "high",
                "notes": null
            }
        ],
        "lois": [
            {
                "label": "LOI Count",
                "value": "3",
                "context": "Enterprise clients",
                "is_projection": false,
                "confidence": "high",
                "notes": null
            },
            {
                "label": "LOI Total Value",
                "value": "$750K",
                "context": "Annual contract value",
                "is_projection": false,
                "confidence": "high",
                "notes": null
            }
        ]
    },
    
    "team": [
        {"name": "John Doe", "role": "CEO", "background": "Ex-Google PM, 10 years in SaaS, MBA from Stanford"},
        {"name": "Jane Smith", "role": "CTO", "background": "Ex-Founder of TechCo (acquired by Microsoft for $50M), Ex-Amazon Engineer"}
    ],
    
    "competition_mentioned": ["Competitor A", "Competitor B", "Competitor C"],
    "competition_note": "Competition as presented in deck may be biased toward favorable comparison",
    
    "observations": [
        "Deck emphasizes rapid growth trajectory",
        "Strong focus on enterprise market",
        "Heavy emphasis on team credentials"
    ],
    
    "unlabeled_claims": [
        "Claims 'industry-leading' without comparative data",
        "States 'proven model' without specific evidence"
    ],
    
    "present_elements": [
        "Problem/Solution slides",
        "Detailed market size analysis (TAM/SAM/SOM)",
        "Team slide with specific backgrounds",
        "Traction metrics with explicit labels",
        "Unit economics breakdown",
        "Funding ask with use of funds"
    ],
    
    "missing_elements": [
        "Competitive analysis beyond names",
        "Detailed go-to-market strategy",
        "Risk factors or challenges",
        "Customer testimonials or case studies"
    ],
    
    "data_quality_notes": "Most metrics are explicitly labeled with high confidence. Some market size figures lack TAM/SAM/SOM distinction. Financial projections are ambitious but backed by current traction data."
}

REMEMBER:
- Extract ALL numbers, even if uncertain - just mark confidence appropriately
- Go into detail (separate seed/series A/B/C, TAM/SAM/SOM, etc.)
- Add notes when something seems unrealistic or needs clarification
- Distinguish facts from projections
- Stay neutral and unbiased
- If uncertain about a label, still include it with medium/low confidence"""


def create_slide_analysis_message(image_base64: str, slide_number: int) -> list:
    """
    Create a message for analyzing a single slide.
    
    Args:
        image_base64: Base64 encoded image
        slide_number: The slide number
    
    Returns:
        List of messages for the vision model
    """
    return [
        HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": f"Slide {slide_number}:\n\n{SLIDE_ANALYSIS_PROMPT}"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_base64}"
                    }
                }
            ]
        )
    ]


def create_deck_summary_message(images_base64: List[str]) -> list:
    """
    Create a message for analyzing the entire deck.
    
    Args:
        images_base64: List of base64 encoded images (all slides)
    
    Returns:
        List of messages for the vision model
    """
    
    content = [
        {
            "type": "text",
            "text": f"Analyze this complete pitch deck ({len(images_base64)} slides):\n\n{DECK_SUMMARY_PROMPT}"
        }
    ]
    
    # Add all slides as images
    for i, img_b64 in enumerate(images_base64, start=1):
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{img_b64}",
                "detail": "high"
            }
        })
    
    return [HumanMessage(content=content)]
