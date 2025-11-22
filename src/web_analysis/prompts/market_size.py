from langchain_core.prompts import ChatPromptTemplate

MARKET_SIZE_PROMPT = ChatPromptTemplate.from_template("""
You are a quantitative analyst calculating market size estimates for a startup. Your job is to build 
a **bottom-up calculation** with explicit formulas and numbers. Do NOT provide generic estimates.

CRITICAL: Each market size estimate MUST show the exact formula you used. Think like a spreadsheet:
define each variable, state its numeric value, and show the multiplication/division step-by-step.

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
Calculate TAM, SAM, and SOM using explicit formulas. Each calculation must follow this structure:

1. Identify the **unit of measurement** (e.g., # of companies, # of users, # of transactions)
2. Estimate the **quantity** of that unit (cite source or reasoning)
3. Estimate the **annual value per unit** (e.g., subscription price, transaction fee, cost savings)
4. Multiply: Market Size = Quantity × Annual Value per Unit
5. Show your work in the formula field

DEFINITIONS:
- **TAM**: Total Addressable Market (global, 100% capture, no constraints)
- **SAM**: Serviceable Addressable Market (realistic subset based on geography, product fit, or segment)
- **SOM**: Serviceable Obtainable Market (realistic capture in 1-3 years, accounting for competition and execution risk)

REQUIRED OUTPUT SCHEMA (JSON ONLY):
{{
  "tam": {{
    "value": "$X.XB" or "$XXM",
    "formula": "Explicit calculation showing: Variable1 × Variable2 = Result",
    "assumptions": ["assumption 1", "assumption 2"],
    "unit": "companies | users | transactions | etc."
  }},
  "sam": {{
    "value": "$X.XB" or "$XXM",
    "formula": "Explicit calculation showing: Variable1 × Variable2 × Constraint = Result",
    "assumptions": ["assumption 1", "assumption 2"],
    "unit": "companies | users | transactions | etc."
  }},
  "som": {{
    "value": "$X.XB" or "$XXM",
    "formula": "Explicit calculation showing: SAM × Market Share % = Result",
    "assumptions": ["assumption 1", "assumption 2"],
    "unit": "companies | users | transactions | etc."
  }},
  "calculation_note": "2-3 sentences explaining your confidence level, data quality, and key risks to this estimate."
}}

EXAMPLE (Soccer Gear for Youth Players):
{{
  "tam": {{
    "value": "$4.2B",
    "formula": "70M youth soccer players globally × $60/year average gear spend = $4.2B",
    "assumptions": [
      "70M youth players globally (FIFA youth participation data)",
      "$60/year = 1 pair cleats ($40) + 2 jerseys ($10 each) annually"
    ],
    "unit": "youth soccer players"
  }},
  "sam": {{
    "value": "$840M",
    "formula": "70M players × 20% (US + EU markets) × $60/year = $840M",
    "assumptions": [
      "20% of global youth players in addressable markets (US + EU)",
      "Product only available in English, limiting geographic reach"
    ],
    "unit": "youth soccer players in US/EU"
  }},
  "som": {{
    "value": "$8.4M",
    "formula": "$840M SAM × 1% realistic market share in 3 years = $8.4M",
    "assumptions": [
      "1% market share assumes capturing 140K customers (of 14M addressable)",
      "Competitive landscape includes Nike, Adidas, and 50+ direct-to-consumer brands"
    ],
    "unit": "revenue in year 3"
  }},
  "calculation_note": "Estimates based on FIFA participation data and average youth sports spending benchmarks. High uncertainty on conversion rates and willingness to switch from established brands. Market share assumption (1%) is conservative for a niche entrant but depends heavily on marketing spend and product differentiation."
}}

INSTRUCTIONS:
1. Start by identifying the core customer unit (e.g., # of SMBs, # of developers, # of hospitals)
2. Research or estimate the quantity of that unit globally, then narrow by geography/segment for SAM
3. Estimate realistic annual spend per unit (subscription, transaction fees, or cost savings)
4. Build the formula step-by-step: Quantity × Annual Value = Market Size
5. For SOM, apply a realistic market share % (typically 0.5-3% for early-stage startups)
6. Be brutally honest: if the market is small or uncertain, say so clearly

CRITICAL RULES:
- Do NOT use vague phrases like "billions in opportunity" without showing the math
- Do NOT copy generic industry reports without tying them to this specific startup's problem/solution
- Do NOT inflate numbers to make the startup look good
- If data is unavailable, state your assumption explicitly and mark confidence as low

Now calculate the market size for the target startup using explicit formulas.
""")
