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


DECK_SUMMARY_PROMPT = """You are analyzing a complete pitch deck. Your role is to extract ALL INFORMATION with appropriate confidence/trustworthiness levels, AND to critically distinguish between FACTS and STORYTELLING.

🚨 CRITICAL INSTRUCTION: CAPTURE AS MUCH INFORMATION AS POSSIBLE - MORE IS BETTER!

CORE PRINCIPLES:
1. EXTRACT ALL NUMBERS - even if labels are vague or missing
2. EXTRACT ALL TEXT CONTENT - customer quotes, case studies, technical details, market insights, EVERYTHING
3. Mark trustworthiness for each data point:
   - "explicit" = Clearly stated with evidence
   - "inferred" = Reasonable interpretation from context
   - "vague" = Unclear or ambiguous (still include it, just mark as vague)
   - "unverifiable" = Claim without supporting evidence (include with note)
4. When information is unconventional or doesn't fit standard categories → capture it in unconventional_data
5. If unsure where something belongs → include it anyway with notes in brackets
6. Distinguish between current facts and projections
7. Present competition AS SHOWN in deck - note that this may be biased
8. DO NOT filter out information - capture everything and let the reader decide
9. For vague or uncertain data, ADD IT with clarifying notes like "(source unclear)" or "(claim unverified)"

TRUSTWORTHINESS LEVELS:

**Explicit** (clearly stated with evidence):
- "Seed Funding: $1.5M from Acme Ventures" ✅
- "MRR: $25K as of Oct 2024" ✅
- Customer quote with name and company ✅
- Patent number with filing date ✅

**Inferred** (reasonable interpretation):
- "Raised $1.5M in 2024" → Likely funding (inferred stage)
- "$25K monthly revenue" → Likely MRR (not explicitly labeled)
- Chart showing growth → Infer metrics (note: "inferred from chart")

**Vague** (unclear but potentially useful):
- "Significant traction" with nearby numbers → (note: "label unclear")
- Unlabeled chart axes → (note: "axes not labeled, appears to show revenue")
- "Major partnership announced" → (note: "partner name not specified")

**Unverifiable** (claim without evidence):
- "Revolutionary technology" → (note: "marketing claim, no technical detail")
- "Market-leading solution" → (note: "claim not substantiated")
- "Proven demand" → (note: "no supporting metrics provided")

COMPREHENSIVE EXTRACTION CATEGORIES:

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
    
    "unconventional_data": [
        {
            "category": "customer_quote",
            "content": "This product saved us 50 hours per week - Jane Doe, CTO at BigCorp",
            "source": "Slide 9",
            "trustworthiness": "explicit",
            "context": "Testimonial from early customer",
            "notes": "No verification link or contact provided"
        },
        {
            "category": "technical_detail",
            "content": "Uses proprietary ML algorithm with 99.7% accuracy on benchmark dataset",
            "source": "Slide 15, Appendix",
            "trustworthiness": "inferred",
            "context": "Technical approach section",
            "notes": "Benchmark dataset not named, accuracy claim unverified"
        },
        {
            "category": "market_insight",
            "content": "Industry spending on [category] grew 45% YoY according to Gartner 2024",
            "source": "Slide 4",
            "trustworthiness": "explicit",
            "context": "Market opportunity slide",
            "notes": "Third-party data cited with source"
        },
        {
            "category": "unusual_metric",
            "content": "Achieved viral coefficient of 1.8",
            "source": "Slide 12",
            "trustworthiness": "vague",
            "context": "Growth slide",
            "notes": "No explanation of how calculated or timeframe"
        }
    ],
    
    "additional_insights": [
        {
            "title": "Detailed Case Study - Enterprise Customer A",
            "description": "Deployed product across 5,000 employees, saw 30% productivity increase in first quarter, measured by internal surveys",
            "source": "Slides 10-11",
            "confidence": "medium",
            "relevance": "Demonstrates enterprise value proposition with quantitative outcomes",
            "flags": ["Productivity metric is self-reported", "Only one detailed case study shown"]
        },
        {
            "title": "Partnership Economics",
            "description": "Channel partner agreement provides access to 500 enterprise customers, revenue share is 70/30 split",
            "source": "Slide 18",
            "confidence": "high",
            "relevance": "Shows clear path to enterprise market via partnerships",
            "flags": []
        }
    ],
    
    "text_heavy_sections": [
        {
            "title": "How It Works - Technical Explanation",
            "content": "Product uses multi-stage pipeline: (1) Data ingestion via API, (2) Real-time processing with proprietary algorithm, (3) ML-based categorization, (4) Automated workflow triggers. System processes 10M events/day with <100ms latency.",
            "slide_numbers": [14, 15],
            "data_type": "technical_explanation",
            "key_takeaways": [
                "Clear technical architecture outlined",
                "Performance metrics specified",
                "Scalability implied by volume claims"
            ],
            "trustworthiness": "inferred",
            "notes": "Technical details provided but no verification possible from deck alone"
        },
        {
            "title": "Go-to-Market Strategy Details",
            "content": "Phase 1 (0-6 months): Direct sales to Fortune 500 via warm introductions. Phase 2 (6-12 months): Launch partner program with 5 system integrators. Phase 3 (12-24 months): Self-serve SMB tier with product-led growth motions.",
            "slide_numbers": [16],
            "data_type": "strategy",
            "key_takeaways": [
                "Phased approach with clear timelines",
                "Multi-channel strategy",
                "Enterprise-first, then down-market"
            ],
            "trustworthiness": "explicit",
            "notes": "Well-articulated strategy but execution risk not addressed"
        }
    ],
    
    "customer_testimonials": [
        "This tool is a game-changer for our team - CEO, TechCorp (slide 9)",
        "We've seen 3x improvement in efficiency - Product Manager, StartupCo (slide 9, note: efficiency metric undefined)"
    ],
    
    "case_studies": [
        "Enterprise A: 5,000 user deployment, 30% productivity increase, 6-month timeline (slides 10-11, note: productivity is self-reported)",
        "SMB Customer B: Reduced manual work from 40hrs/week to 2hrs/week, 95% cost savings (slide 11, note: impressive but n=1)"
    ],
    
    "pilot_programs": [
        "10-company pilot program completed with 8/10 converting to paid, avg contract value $50K (slide 13)",
        "University research collaboration showing 40% improvement in target metric (slide 20, note: university name not disclosed)"
    ],
    
    "market_insights": [
        "Industry spending on [category] expected to reach $50B by 2027 (Gartner, slide 4)",
        "Current solutions have 65% customer dissatisfaction rate according to G2 reviews (slide 5)",
        "Regulatory changes in 2025 will mandate solutions like ours for companies >1000 employees (slide 6, note: regulation not specifically cited)"
    ],
    
    "industry_statistics": [
        "Gartner: Market growing at 35% CAGR (slide 4)",
        "McKinsey study: 70% of companies in sector report [problem] as top 3 challenge (slide 3, note: study year not mentioned)"
    ],
    
    "gtm_strategy_details": "Phase 1: Direct sales to Fortune 500 via founder network and warm intros. Phase 2: Partner channel with system integrators. Phase 3: Product-led growth for SMB segment. Initial focus on financial services vertical, then expand to healthcare and tech.",
    
    "marketing_channels": [
        "LinkedIn outbound (primary channel, 15% response rate mentioned on slide 17)",
        "Industry conferences (3 major events identified)",
        "Content marketing (blog has 10K monthly visitors per slide 17)",
        "Partner referrals (expected to drive 40% of leads by Q4 2026)"
    ],
    
    "sales_strategy": "Enterprise: Direct sales with 6-9 month sales cycle, ACV $100K-$500K. Mid-market: Inside sales with 2-3 month cycle, ACV $25K-$75K. SMB: Self-serve with product-led growth, ACV $5K-$15K (slide 16).",
    
    "technology_stack": [
        "React frontend (slide 15)",
        "Python/Django backend (slide 15)",
        "PostgreSQL database (slide 15)",
        "AWS infrastructure (slide 15)",
        "Proprietary ML models (mentioned but not detailed)"
    ],
    
    "technical_approach": "Multi-layer architecture with API-first design, real-time data processing using proprietary algorithms, ML-based categorization with 99.7% claimed accuracy (unverified), automated workflow engine. Slide 15 has detailed technical diagram.",
    
    "product_roadmap": [
        "Q1 2026: Mobile app launch",
        "Q2 2026: AI co-pilot feature (described as 'game-changing' - marketing language)",
        "Q3 2026: Enterprise admin dashboard",
        "Q4 2026: International expansion to EU markets"
    ],
    
    "integration_partners": [
        "Salesforce (integration live, slide 18)",
        "Slack (integration live, slide 18)",
        "Microsoft Teams (planned Q1 2026, slide 18)",
        "Zoom (in discussion, slide 18)"
    ],
    
    "risks_acknowledged": [
        "Market competition intensifying (slide 22)",
        "Regulatory uncertainty in EU markets (slide 22, note: good they acknowledge this)"
    ],
    
    "mitigation_strategies": [
        "Building defensible IP moat via patents (3 filed, slide 22)",
        "Locking in customers with multi-year contracts (slide 22)"
    ],
    
    "press_coverage": [
        "Featured in TechCrunch article May 2024 (slide 19)",
        "Forbes '30 Under 30' for CEO (slide 19)",
        "VentureBeat coverage of product launch (slide 19, no link provided)"
    ],
    
    "thought_leadership": [
        "CEO spoke at SaaStr conference 2024 (slide 19)",
        "Published whitepaper with 5,000 downloads (slide 19, note: topic not specified)"
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
        "Financial projections with assumptions",
        "Customer case studies and testimonials",
        "Technical architecture details",
        "Go-to-market strategy with phases",
        "Product roadmap",
        "Risk acknowledgment section"
    ],
    
    "missing_elements": [
        "Detailed competitive response strategy",
        "Customer retention/churn data over time",
        "Detailed hiring plan with roles and timeline",
        "International expansion costs",
        "Customer acquisition cost by channel breakdown"
    ],
    
    "data_quality_notes": "Most metrics are explicitly labeled with high confidence. Funding breakdown is detailed with clear separation of dilutive vs. non-dilutive sources. Some projections lack supporting assumptions. Business model section is comprehensive. IP claims are well-documented with patent numbers. Some marketing claims lack quantitative backing. Significant amount of unconventional data captured including technical details, customer quotes, and market insights. Text-heavy sections provide good context but some claims are unverifiable from deck alone.",
    
    "deck_quality_assessment": "Comprehensive deck with strong quantitative backing for most claims. Good balance of high-level narrative and detailed data. Technical depth is notable. Some aspirational language but mostly grounded in metrics. Could benefit from more explicit labeling on certain charts.",
    
    "notable_strengths": [
        "Detailed business model breakdown with specific pricing",
        "Comprehensive technical architecture explanation",
        "Multiple case studies with quantitative outcomes",
        "Well-documented IP portfolio with patent numbers",
        "Realistic acknowledgment of risks and competition",
        "Clear phased go-to-market strategy"
    ],
    
    "notable_weaknesses": [
        "Some projections lack detailed supporting assumptions",
        "Limited discussion of competitive response if competitors catch up",
        "Customer testimonials lack verification links or contacts",
        "Some industry statistics cited without specific study references",
        "Viral coefficient claim needs more explanation of calculation"
    ]
}

REMEMBER:
- Extract ALL information, even unconventional or unusual data
- Use unconventional_data for anything that doesn't fit standard categories
- Use additional_insights for interesting findings that provide context
- Use text_heavy_sections for detailed explanations, methodologies, case studies
- Mark trustworthiness honestly: explicit, inferred, vague, unverifiable
- Add clarifying notes in brackets when data seems questionable: "(claim unverified)", "(metric undefined)", "(source not cited)"
- MORE INFORMATION IS BETTER - don't filter, just label appropriately
- Go into DETAILED analysis (separate seed/series A/B/C, TAM/SAM/SOM, etc.)
- CRITICALLY ANALYZE PROJECTIONS vs. CURRENT STATE
- DISTINGUISH FACTS from STORYTELLING: what's verifiable vs. marketing narrative
- Stay neutral and unbiased
- Be thorough and comprehensive - capture everything visible in the deck"""


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
