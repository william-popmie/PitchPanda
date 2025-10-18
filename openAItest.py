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
    
    prompt = f"""I am part of a VC firm as a university intern and need to go through 40 startups a week and evaluate them on wether we should invest in them or not. Please help me with this process. I have fetched the content from the company website below. Give a very brief overview of the company: what they do, the problem they are solving and the solution they are providing. These three things need to be short and intuitive.

After that also list me the names of the founders. If you can't find these in the website content, use your knowledge to search for founder information about this company, but look thoroughly for them

Finally: list competitors for the given startup. Explain why they are competition and what they do the same and different. If they are literally doing exactly the same, even better. If they do like one or a couple things different, list them as well. The more the better with very brief explenations

Company URL: {company_url}

Website Content:
{website_content}"""
    
    print("Analyzing with GPT-5...")
    client = ChatOpenAI(model_name="gpt-5", temperature=0.5)
    response = client.invoke([HumanMessage(content=prompt)])
    return response.content


if __name__ == "__main__":
    # Change this URL to analyze a different startup
    company_url = "https://www.chartera.io/"
    
    print("Analyzing startup...")
    result = analyze_startup(company_url)
    
    # Save to RESULT.md
    with open("RESULT.md", "w", encoding="utf-8") as f:
        f.write(result)
    
    print("✓ Analysis complete! Output saved to: RESULT.md")
    print(f"\n{result}")
