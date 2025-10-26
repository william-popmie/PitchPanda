from csv_utils import read_pitches_csv
from openAItest import analyze_startup
from utils import slugify, ensure_directory_exists


if __name__ == "__main__":
    # Read startups from CSV file
    try:
        startups = read_pitches_csv("input/Pitches.csv")
        print(f"Found {len(startups)} startups to analyze\n")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading CSV file: {e}")
        exit(1)

    # Ensure output directory exists
    output_dir = "output"
    ensure_directory_exists(output_dir)
    
    all_results = []
    successful_analyses = 0
    failed_analyses = 0
    
    # Analyze each startup
    for i, startup in enumerate(startups, 1):
        company_name = startup['name']
        company_url = startup['url']
        print(f"[{i}/{len(startups)}] Analyzing: {company_name} ({company_url})")
        
        # Generate filename with number and slugified name
        slug = slugify(company_name)
        filename = f"result-{i:02d}-{slug}.md"
        filepath = f"{output_dir}/{filename}"
        
        try:
            result = analyze_startup(company_url)
            
            # Prepare the content for individual file
            content = f"# {company_name}\n\n"
            content += f"**URL**: {company_url}\n\n"
            content += f"**Analysis Date**: {i}/{len(startups)}\n\n"
            content += "---\n\n"
            content += result
            
            # Save individual result file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            # Also add to combined results
            all_results.append(f"# Analysis {i}: {company_name}\n\n**URL**: {company_url}\n\n{result}\n\n{'='*80}\n")
            
            successful_analyses += 1
            print(f"✓ Completed {i}/{len(startups)} - Saved to {filename}\n")
            
        except Exception as e:
            # Save error to individual file
            error_content = f"# {company_name}\n\n"
            error_content += f"**URL**: {company_url}\n\n"
            error_content += f"**Analysis Date**: {i}/{len(startups)}\n\n"
            error_content += "---\n\n"
            error_content += f"**ERROR**: Failed to analyze - {str(e)}\n"
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(error_content)
            
            # Also add to combined results
            error_msg = f"# Analysis {i}: {company_name}\n\n**URL**: {company_url}\n\n**ERROR**: Failed to analyze - {str(e)}\n\n{'='*80}\n"
            all_results.append(error_msg)
            
            failed_analyses += 1
            print(f"✗ Error analyzing {company_name}: {e}\n")
    
    # Save combined results to one file
    with open("RESULT.md", "w", encoding="utf-8") as f:
        f.write("# Startup Analysis Report\n\n")
        f.write(f"Total startups analyzed: {len(startups)}\n")
        f.write(f"Successful: {successful_analyses} | Failed: {failed_analyses}\n\n")
        f.write("="*80 + "\n\n")
        f.writelines(all_results)

    print("="*80)
    print(f"✓ All analyses complete!")
    print(f"✓ Individual results saved to: {output_dir}/")
    print(f"✓ Combined report saved to: RESULT.md")
    print(f"✓ Analyzed {len(startups)} startups ({successful_analyses} successful, {failed_analyses} failed)")