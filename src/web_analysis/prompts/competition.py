from langchain_core.prompts import ChatPromptTemplate

COMP_PROMPT = ChatPromptTemplate.from_template("""
You are an evidence-driven AI analyst. Using the target startup's validated profile below, return 5–10 competing startups
that solve the same user problem (problem similarity should be near-identical). Focus on companies that demonstrate the
problem/solution fit on their product pages, docs, case studies, or pricing pages. Do not invent competitors — only include
companies that have verifiable public evidence for the claims below.

TARGET STARTUP (ground truth):
- Name: {startup_name}
- URL: {startup_url}

Problem (general): {problem_general}
Problem (example): {problem_example}

Solution (what_it_is): {solution_what}
Solution (how_it_works): {solution_how}
Solution (example): {solution_example}

Product type: {product_type}
Sector/Subsector: {sector} / {subsector}
Active locations: {active_locations}

---

INSTRUCTIONS
- Return JSON ONLY in this exact structure:
{{
  "competition": [
    {{
      "name": "Company A",
      "website": "https://...",
      "product_type": "SaaS | App | Platform | API | Service | Hardware | Marketplace | Other",
      "sector": "Broad industry",
      "subsector": "Specific niche",
      "problem_similarity": "1–2 lines explaining the overlap in problem focus (cite where this is stated on their site).",
      "solution_summary": "2–4 lines summarizing their solution and mechanism (cite feature/page).",
      "similarities": ["bullet 1 (with short evidence)", "bullet 2 (with short evidence)"],
      "differences": ["bullet 1 (with short evidence)", "bullet 2 (with short evidence)"],
      "active_locations": ["Country/Region/City"],
      "sources": ["https://... (exact page used as evidence)"] ,
      "confidence": "high | medium | low",
      "why_included": "One-line justification linking the target's problem to this company's product messaging (cite source)."
    }}
  ]
}}

REQUIRED GUIDELINES
- Only include companies that have PUBLIC evidence (website, docs, press) demonstrating they address the same problem or ICP.
- For each competitor: explicitly state the exact place you found the evidence in `sources` and include a short `why_included` line.
- `problem_similarity` must make a direct connection to the target's problem (e.g., "Both target SMB logistics teams lacking real-time ETA for local deliveries"), preferably with a quoted phrase or paraphrase from the competitor page.
- `solution_summary` must clearly state how their solution addresses the problem and whether it matches the target's approach or differs (explain difference).
- `similarities` and `differences` should be concise bullets with short evidence markers (e.g., "targets same ICP (homepage hero)" or "API-first vs full product (pricing/docs)").
- Set `confidence` to `high` when the competitor's site explicitly states the same problem/ICP or shows a product page matching the capability; `medium` when inferred from case studies or blog posts; `low` when evidence is sparse.
- If you cannot find 5 credible matches, return only the credible ones (do not invent entries).
- Deduplicate by company domain.

OUTPUT QUALITY
- Prioritize accuracy over quantity. If a company looks similar but you cannot find a clear page or product evidence, omit it.
- If the competitor is an adjacent or partial competitor, mark that clearly in `differences` and set `confidence` accordingly.

Now return the JSON.
""")
