"""Simple startup analyzer using LangChain + OpenAI (gpt-4o).

Install:
  pip install langchain langchain-openai python-dotenv requests beautifulsoup4
"""

import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from utils import normalize_url


API_KEY = os.getenv("PITCH_PANDA_API_KEY") or os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("PITCH_PANDA_API_KEY not set. Copy .env.example to .env and set the key.")

os.environ["OPENAI_API_KEY"] = API_KEY


def fetch_website_content(url: str) -> str:
    """Fetch and extract text content from a website."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script, style, and navigation elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Get title
        title = soup.title.string if soup.title else ""
        
        # Get meta description
        meta_desc = ""
        meta_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if meta_tag and meta_tag.get("content"):
            meta_desc = meta_tag.get("content")
        
        # Get main content
        main_content = soup.find("main") or soup.find("article") or soup.body
        if main_content:
            texts = []
            for tag in main_content.find_all(['h1', 'h2', 'h3', 'p', 'li'], limit=100):
                text = tag.get_text(strip=True)
                if text and len(text) > 20:
                    texts.append(text)
            content = "\n".join(texts[:50])
        else:
            content = soup.get_text(separator="\n", strip=True)[:5000]
        
        return f"Title: {title}\n\nMeta Description: {meta_desc}\n\nWebsite Content:\n{content}"
    
    except Exception as e:
        return f"Error fetching website: {str(e)}"


def analyze_startup(company_url: str) -> str:
    """Fetch website content and send analysis prompt to GPT-4o."""
    
    print("Fetching website content...")
    website_content = fetch_website_content(company_url)
    
    prompt = f"""You are an analyst helping a VC firm evaluate startups. Your role is to **inform, not pitch**. Be honest, factual, and clear. Don't make the startup sound better or worse than it is.

Analyze the startup based on the website content below and structure your response EXACTLY as follows:

## Problem
Explain the core problem the startup is solving. Be intuitive and understandable. 1-2 short paragraphs max.

## Solution
Summarize how their product solves the problem. Use examples if helpful, but keep it clear and concise. 1-2 short paragraphs max.

## Market Advantage
Assess if their advantage is defensible. Consider: proprietary tech, IP, speed to market, regulations, partnerships, network effects, or customer lock-in. Be honest—if there's no clear moat, say so. 1-2 short paragraphs max.

## Team
List core team members with:
- Name, role
- LinkedIn URL (only if you can confidently find it—don't guess)
- Prior relevant and/or irrelevant experience (previous roles/companies)
- Previous **founder** experience (if any)

Use your knowledge to find team information if not on the website. Format as a clean list.

## Things to Consider
List concerns, red flags, or positive signals an investor would find relevant. Be factual and balanced. Examples:
- "No live product yet"
- "Founders previously scaled X to 5M users"
- "High customer acquisition cost in this market"
- "Strong early traction (X customers in Y months)"

Use bullet points. 3-7 items.

## Competition
Create a markdown table of direct competitors:

| Company | Website | Region | Same | Different |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

**Be honest**: If a competitor does exactly the same thing, say so in "Same" and put "None" or "-" in "Different". Don't make this startup sound better than it is. The goal is to inform, not pitch. Be clear and specific about what they do the same and what they do differently.

---

Company URL: {company_url}

Website Content:
{website_content}

Remember: Be clear, factual, and informative. Don't oversell or undersell."""
    
    print("Analyzing with GPT-5...")
    client = ChatOpenAI(model_name="gpt-5", temperature=0.3)
    response = client.invoke([HumanMessage(content=prompt)])
    return response.content


if __name__ == "__main__":
    # Change this URL to analyze a different startup
    company_url = normalize_url("https://www.supercity.ai")
    
    print("Analyzing startup...")
    result = analyze_startup(company_url)
    
    # Save to RESULT.md
    with open("RESULT.md", "w", encoding="utf-8") as f:
        f.write(result)
    
    print("✓ Analysis complete! Output saved to: RESULT.md")
    print(f"\n{result}")
