from langchain_core.prompts import ChatPromptTemplate

MARKET_SIZE_PROMPT = ChatPromptTemplate.from_template("""
You are an AI analyst calculating market size estimates for a startup. Your goal is to provide 
**objective, reasonable estimates** based on the startup's problem and solution.

IMPORTANT: Do NOT try to sell or pitch this startup. Provide conservative, calculated estimates 
with clear reasoning. If the market seems small, say so. If it's uncertain, acknowledge that.

TARGET STARTUP:
- Name: {startup_name}
- URL: {startup_url}

Problem (general): {problem_general}
Problem (example): {problem_example}

Solution (what_it_is): {solution_what}
Solution (how_it_works): {solution_how}

Product type: {product_type}
Sector/Subsector: {sector} / {subsector}
Active locations: {active_locations}

---

TASK:
Calculate TAM (Total Addressable Market), SAM (Serviceable Addressable Market), and SOM 
(Serviceable Obtainable Market) for this startup.

GUIDELINES:
1. **Be objective and conservative** - don't inflate numbers to make the startup look good
2. **Show your work** - explain the calculation methodology clearly
3. **State assumptions** - what data points or market research did you use?
4. **Include caveats** - what could make these numbers wrong?
5. **Use real market data when possible** - reference industry reports, market sizes, etc.
6. **Consider geography** - if they're only in certain locations, adjust accordingly
7. **Be realistic about SOM** - this should be a small fraction of SAM for early-stage startups

APPROACH:
- **TAM**: The total revenue opportunity if the startup captured 100% of their target market globally
- **SAM**: The portion of TAM the startup can realistically serve given their product and geography
- **SOM**: The portion of SAM the startup could realistically capture in the near term (1-3 years)

Each estimate should include:
- A numerical range (e.g., "$50M - $150M" or "10,000 - 25,000 potential customers")
- Brief context on how you arrived at this number

Return JSON ONLY with this schema:
{{
  "tam": "Numerical estimate with brief context (1-2 sentences)",
  "sam": "Numerical estimate with brief context (1-2 sentences)", 
  "som": "Numerical estimate with brief context (1-2 sentences)",
  "calculation_context": "Detailed explanation (3-5 sentences) of your methodology, assumptions, data sources, and key drivers of the calculation. Be specific about what numbers you multiplied/divided and why.",
  "note": "Caveats and disclaimers about the accuracy of these estimates (2-3 sentences)"
}}

EXAMPLE OUTPUT STYLE:
{{
  "tam": "$2.5B - $4B annually. Based on the global B2B SaaS market for small business inventory management (~500K businesses × $5K-$8K annual contract value).",
  "sam": "$150M - $300M annually. Focusing on English-speaking markets (Belgium, Netherlands, UK) where they're currently active, approximately 30K small retailers × $5K-$10K ACV.",
  "som": "$3M - $8M annually. Realistically capturing 1-2% of SAM in first 3 years (300-600 customers at $10K ACV), assuming moderate growth and competition from established players.",
  "calculation_context": "TAM calculated using estimated 500K small retailers globally facing inventory challenges, multiplied by typical SaaS contract values in this segment ($5K-$8K based on comparable tools). SAM narrowed to active geographies (Benelux + UK) representing ~6-8% of global market. SOM assumes conservative 1-2% market penetration in 3 years, typical for bootstrapped B2B SaaS startups facing established competition. Key assumptions: comparable pricing to existing tools, steady customer acquisition, and similar retention rates to industry benchmarks.",
  "note": "These estimates are highly uncertain and based on limited public data. Actual market size depends heavily on product-market fit, pricing strategy, and competitive dynamics. The retail tech market is crowded, so customer acquisition costs may be higher than assumed. Recommend validating with bottom-up customer research and actual conversion data."
}}

Now calculate the market size for the target startup.
""")
