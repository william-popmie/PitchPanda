from csv_utils import read_pitches_csv
from openAItest import analyze_startup


if __name__ == "__main__":
    # Read startups from CSV file
    try:
        startups = read_pitches_csv("input/Pitches.csv")
        print(f"Found {len(startups)} startups to analyze\n")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading CSV file: {e}")
        exit(1)

    all_results = []
    
    # Analyze each startup
    for i, startup in enumerate(startups, 1):
        company_name = startup['name']
        company_url = startup['url']
        print(f"[{i}/{len(startups)}] Analyzing: {company_name} ({company_url})")
        
        try:
            result = analyze_startup(company_url)
            all_results.append(f"# Analysis {i}: {company_name}\n\n**URL**: {company_url}\n\n{result}\n\n{'='*80}\n")
            print(f"✓ Completed {i}/{len(startups)}\n")
        except Exception as e:
            error_msg = f"# Analysis {i}: {company_name}\n\n**URL**: {company_url}\n\n**ERROR**: Failed to analyze - {str(e)}\n\n{'='*80}\n"
            all_results.append(error_msg)
            print(f"✗ Error analyzing {company_name}: {e}\n")
    
    # Save all results to one file
    with open("RESULT.md", "w", encoding="utf-8") as f:
        f.write("# Startup Analysis Report\n\n")
        f.write(f"Total startups analyzed: {len(startups)}\n\n")
        f.write("="*80 + "\n\n")
        f.writelines(all_results)

    print("="*80)
    print(f"✓ All analyses complete! Output saved to: RESULT.md")
    print(f"✓ Analyzed {len(startups)} startups")