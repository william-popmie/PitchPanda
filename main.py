from pdf_utils import extractLinks
from openAItest import analyze_startup


if __name__ == "__main__":
    # Extract all the links from the pdf
    links = extractLinks("./Pitches.pdf")
    print(f"Found {len(links)} startup links to analyze\n")

    all_results = []
    
    # Analyze each startup
    for i, company_url in enumerate(links, 1):
        print(f"[{i}/{len(links)}] Analyzing: {company_url}")
        
        try:
            result = analyze_startup(company_url)
            all_results.append(f"# Analysis {i}: {company_url}\n\n{result}\n\n{'='*80}\n")
            print(f"✓ Completed {i}/{len(links)}\n")
        except Exception as e:
            error_msg = f"# Analysis {i}: {company_url}\n\n**ERROR**: Failed to analyze - {str(e)}\n\n{'='*80}\n"
            all_results.append(error_msg)
            print(f"✗ Error analyzing {company_url}: {e}\n")
    
    # Save all results to one file
    with open("RESULT.md", "w", encoding="utf-8") as f:
        f.write("# Startup Analysis Report\n\n")
        f.write(f"Total startups analyzed: {len(links)}\n\n")
        f.write("="*80 + "\n\n")
        f.writelines(all_results)

    print("="*80)
    print(f"✓ All analyses complete! Output saved to: RESULT.md")
    print(f"✓ Analyzed {len(links)} startups")