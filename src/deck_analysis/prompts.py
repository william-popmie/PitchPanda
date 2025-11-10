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


DECK_SUMMARY_PROMPT = """You are analyzing a complete pitch deck. Your role is to extract ALL METRICS AND NUMBERS with appropriate confidence levels, AND to critically distinguish between FACTS and STORYTELLING.

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
8. EXTRACT COMPETITIVE ADVANTAGES: patents (secured/pending), IP, trade secrets, exclusive partnerships, regulatory approvals
9. EXTRACT AWARDS & GRANTS: government grants, accelerator programs, competition wins, non-dilutive funding
10. ANALYZE BUSINESS MODEL IN DEPTH: revenue model, pricing, customer acquisition, partnerships, distribution
11. CRITICALLY ANALYZE PROJECTIONS: separate what's stated as fact vs. aspirational claims
12. DISTINGUISH FACTS FROM STORYTELLING: What can be verified vs. what's marketing narrative

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

**Funding (go into DETAILED breakdown):**
- Pre-Seed, Seed, Series A/B/C/D (separate each round)
- Bridge Round, Convertible Note, SAFE
- Total Raised, Current Round Target, Amount Seeking
- Valuation (Pre-Money, Post-Money)
- Runway (months), Burn Rate
- Investor names/firms if mentioned
- NON-DILUTIVE funding: government grants, R&D tax credits, revenue-based financing
- Use of funds breakdown if shown

**Awards & Grants:**
- Government grants (SBIR, STTR, EU grants, etc.)
- Accelerator programs (Y Combinator, Techstars, etc.)
- Competition wins and prizes
- Industry awards or recognition
- Academic or research grants
- Non-dilutive funding sources
- Amounts and dates if mentioned

**Competitive Advantages (IP & Moats):**
- Patents Secured: patent numbers, filing dates, jurisdictions
- Patents Pending: provisional or full applications
- Trade Secrets: proprietary technology or processes
- Exclusive Partnerships: exclusive agreements or distribution rights
- Regulatory Approvals: FDA clearance, certifications, licenses
- Proprietary Data or Algorithms
- Network Effects mentioned
- First-mover advantages claimed
- Barriers to entry identified

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
- Conversion probability if mentioned

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

**Business Model (DETAILED analysis):**
- Revenue Model: subscription, transaction fee, licensing, marketplace, etc.
- Pricing Structure: specific tiers, per-user pricing, enterprise vs. SMB
- Customer Acquisition: channels, CAC by channel, strategies
- Sales Cycle: length, process, bottlenecks
- Partnerships: strategic partners, integration partners, channel partners
- Distribution Channels: direct sales, partnerships, self-serve, etc.
- Expansion Strategy: geographic, vertical, horizontal
- Moats and defensibility beyond IP
- Unit economics breakdown
- Path to profitability if discussed

**Team:**
- Names, Roles (CEO, CTO, COO, CFO, etc.)
- Previous Experience (be specific: "Ex-Google Engineer", "Former Founder of X (acquired by Y)")
- Years of experience in industry
- Notable exits, IPOs, acquisitions
- Advisory board members if mentioned
- Key hires or talent density claims

**Competition:**
- Competitors mentioned
- Market positioning claims
- Competitive advantages claimed (may be biased)

EXTRACTION FORMAT:

Return JSON in this exact structure:
{
    "problem_statement": "Brief factual description of problem",
    "solution_overview": "Brief factual description of solution",
    "value_proposition": "Value prop as stated",
    "target_market": "Target market as described",
    "business_model": "High-level: How they make money",
    
    "business_model_details": {
        "revenue_model": "Subscription, transaction fee, licensing, etc.",
        "pricing_structure": "Specific pricing tiers if mentioned",
        "customer_acquisition": "How they acquire customers (channels, strategies)",
        "sales_cycle": "Length and process if discussed",
        "partnerships": ["Partner A", "Partner B"],
        "distribution_channels": ["Direct sales", "Channel partners", "Self-serve"],
        "expansion_strategy": "Geographic or market expansion plans",
        "notes": [
            "Additional insight about their business model",
            "Observations about sustainability or scalability"
        ]
    },
    
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
            }
        ],
        "traction": [...],
        "market_size": [...],
        "financials": [...],
        "lois": [...]
    },
    
    "funding_details": [
        {
            "type": "seed",
            "amount": "$1.5M",
            "date": "Q1 2024",
            "investors": ["Acme Ventures", "Angel Investor Group"],
            "is_non_dilutive": false,
            "valuation": "$10M post-money",
            "notes": null
        },
        {
            "type": "grant",
            "amount": "$250K",
            "date": "2023",
            "investors": ["NSF SBIR Phase I"],
            "is_non_dilutive": true,
            "valuation": null,
            "notes": "Government R&D grant"
        }
    ],
    
    "competitive_advantages": [
        {
            "category": "patent_secured",
            "description": "AI-based recommendation algorithm",
            "status": "granted",
            "details": "US Patent #10,123,456 filed 2022, granted 2024",
            "confidence": "high"
        },
        {
            "category": "patent_pending",
            "description": "Blockchain-based verification system",
            "status": "pending",
            "details": "Provisional patent filed Q3 2024",
            "confidence": "high"
        },
        {
            "category": "exclusive_partnership",
            "description": "Exclusive distribution agreement with MajorCorp",
            "status": "active",
            "details": "3-year exclusive for North American market",
            "confidence": "high"
        },
        {
            "category": "regulatory_approval",
            "description": "FDA 510(k) clearance",
            "status": "granted",
            "details": "Received clearance in 2024 for Class II medical device",
            "confidence": "high"
        },
        {
            "category": "proprietary_technology",
            "description": "Proprietary data pipeline claimed but not verified",
            "status": null,
            "details": null,
            "confidence": "medium"
        }
    ],
    
    "awards_and_grants": [
        {
            "type": "grant",
            "name": "NSF SBIR Phase I",
            "amount": "$250K",
            "year": "2023",
            "organization": "National Science Foundation",
            "is_non_dilutive": true
        },
        {
            "type": "accelerator",
            "name": "Y Combinator S23",
            "amount": "$500K",
            "year": "2023",
            "organization": "Y Combinator",
            "is_non_dilutive": false
        },
        {
            "type": "award",
            "name": "Best AI Startup 2024",
            "amount": null,
            "year": "2024",
            "organization": "Tech Innovation Awards",
            "is_non_dilutive": null
        },
        {
            "type": "competition_win",
            "name": "Startup Pitch Competition Winner",
            "amount": "$50K",
            "year": "2024",
            "organization": "Tech Conference X",
            "is_non_dilutive": true
        }
    ],
    
    "team": [
        {"name": "John Doe", "role": "CEO", "background": "Ex-Google PM, 10 years in SaaS, MBA from Stanford"},
        {"name": "Jane Smith", "role": "CTO", "background": "Ex-Founder of TechCo (acquired by Microsoft for $50M), Ex-Amazon Engineer"}
    ],
    
    "competition_mentioned": ["Competitor A", "Competitor B", "Competitor C"],
    "competition_note": "Competition as presented in deck may be biased toward favorable comparison",
    
    "projection_analysis": [
        {
            "metric_name": "ARR",
            "current_value": "$100K",
            "projected_value": "$5M",
            "timeframe": "By end of 2026",
            "assumptions_stated": [
                "15% MoM growth continues",
                "Enterprise contracts convert at 80%",
                "New product launch in Q2 2026"
            ],
            "realism_assessment": "Ambitious but possible if enterprise pipeline converts. 50x growth in 2 years is aggressive given current trajectory.",
            "supporting_evidence": [
                "Current MoM growth is 15%",
                "3 enterprise LOIs worth $2M combined"
            ],
            "flags": [
                "No discussion of increased CAC with scale",
                "Assumes no competitive response",
                "Market conditions assumed to remain favorable"
            ]
        },
        {
            "metric_name": "User Growth",
            "current_value": "5,000 users",
            "projected_value": "500,000 users",
            "timeframe": "18 months",
            "assumptions_stated": [],
            "realism_assessment": "100x user growth with no stated assumptions or supporting strategy is a red flag.",
            "supporting_evidence": [],
            "flags": [
                "No clear explanation of how growth will be achieved",
                "No marketing budget or CAC assumptions provided",
                "Viral coefficient not mentioned"
            ]
        }
    ],
    
    "facts": [
        "Raised $1.5M seed round in Q1 2024 from Acme Ventures (verified on slide 8)",
        "Currently generating $50K MRR as of October 2025 (chart on slide 12)",
        "Has 3 signed LOIs totaling $750K ACV (slide 14 shows specific customers)",
        "Team has 2 prior successful exits (backed by LinkedIn profiles shown)",
        "FDA 510(k) clearance granted in March 2024 (clearance number provided)"
    ],
    
    "storytelling": [
        "Claims to be 'revolutionizing the industry' without specific evidence",
        "States 'massive market opportunity' but TAM calculation methodology not explained",
        "Describes product as '10x better' than competitors with no comparative data",
        "Claims 'proven product-market fit' but limited customer validation shown",
        "Projects $100M revenue in 3 years without detailed unit economics to support",
        "Uses phrases like 'disruptive technology' and 'game-changing solution' without substantiation"
    ],
    
    "observations": [
        "Deck emphasizes rapid growth trajectory",
        "Strong focus on enterprise market",
        "Heavy emphasis on team credentials",
        "Business model details are comprehensive with specific pricing tiers",
        "Multiple non-dilutive funding sources demonstrate resourcefulness",
        "Patent portfolio suggests defensible technology moat"
    ],
    
    "unlabeled_claims": [
        "Claims 'industry-leading' without comparative data",
        "States 'proven model' without specific evidence",
        "Chart on slide 7 has no axis labels - unclear what is being measured"
    ],
    
    "present_elements": [
        "Problem/Solution slides",
        "Detailed market size analysis (TAM/SAM/SOM)",
        "Team slide with specific backgrounds",
        "Traction metrics with explicit labels",
        "Unit economics breakdown",
        "Funding ask with use of funds",
        "Intellectual property section",
        "Awards and recognition slide",
        "Detailed business model canvas",
        "Competitive landscape matrix",
        "Financial projections with assumptions"
    ],
    
    "missing_elements": [
        "Customer testimonials or case studies",
        "Detailed go-to-market strategy beyond high-level",
        "Risk factors or challenges section",
        "Competitive response strategy",
        "Detailed hiring plan"
    ],
    
    "data_quality_notes": "Most metrics are explicitly labeled with high confidence. Funding breakdown is detailed with clear separation of dilutive vs. non-dilutive sources. Some projections lack supporting assumptions. Business model section is comprehensive. IP claims are well-documented with patent numbers. Some marketing claims lack quantitative backing."
}

REMEMBER:
- Extract ALL numbers, even if uncertain - just mark confidence appropriately
- Go into DETAILED analysis (separate seed/series A/B/C, TAM/SAM/SOM, etc.)
- EXTRACT IP & COMPETITIVE ADVANTAGES: patents, trade secrets, regulatory approvals
- EXTRACT AWARDS & GRANTS: especially non-dilutive funding sources
- ANALYZE BUSINESS MODEL IN DEPTH: pricing, channels, partnerships, expansion strategy
- CRITICALLY ANALYZE PROJECTIONS vs. CURRENT STATE
- DISTINGUISH FACTS from STORYTELLING: what's verifiable vs. marketing narrative
- Add notes when something seems unrealistic or needs clarification
- Stay neutral and unbiased
- Be critical but fair in assessing claims vs. evidence"""


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
