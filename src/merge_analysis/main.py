"""
Main runner for merge analysis.

Merges deck analysis and web analysis into a comprehensive company overview.

Usage:
    python -m src.merge_analysis.main
    
Or with a specific company output directory:
    python -m src.merge_analysis.main output/company-name
"""
import os
import sys
from pathlib import Path

from .graph import merge_graph, MergeState
from .renderer import render_markdown
from .schemas import MergedAnalysis
from ..core.utils import ensure_dir


# Default paths
OUTPUT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "output")
)


def merge_company_analysis(company_dir: str) -> bool:
    """
    Merge deck and web analysis for a company.
    
    Args:
        company_dir: Path to company output directory (e.g., output/company-name)
        
    Returns:
        True if successful, False otherwise
    """
    company_name = os.path.basename(company_dir)
    
    print(f"\n{'='*60}")
    print(f"Merging Analysis: {company_name}")
    print(f"{'='*60}\n")
    
    # Check for input files
    deck_path = os.path.join(company_dir, "deck_analysis.md")
    web_path = os.path.join(company_dir, "web_analysis.md")
    
    deck_exists = os.path.exists(deck_path)
    web_exists = os.path.exists(web_path)
    
    if not deck_exists and not web_exists:
        print(f"No analysis files found in {company_dir}")
        return False
    
    print(f"Found:")
    if deck_exists:
        print(f"Pitch deck analysis")
    if web_exists:
        print(f"Web analysis")
    print()
    
    # Create initial state
    state = MergeState(
        company_name=company_name,
        deck_analysis_path=deck_path if deck_exists else None,
        web_analysis_path=web_path if web_exists else None,
    )
    
    # Run the merge graph
    try:
        result = merge_graph.invoke(state)
        
        # Extract the merged analysis
        if isinstance(result, dict):
            merged_data = result.get("merged_analysis")
        else:
            merged_data = result.merged_analysis
        
        if not merged_data:
            print("Failed to generate merged analysis")
            return False
        
        # Convert to schema object
        merged_analysis = MergedAnalysis(**merged_data)
        
        # Render to markdown
        print("Rendering merged analysis...")
        md_content = render_markdown(merged_analysis)
        
        # Save to file
        output_path = os.path.join(company_dir, "merged_analysis.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"Saved to: {output_path}")
        print()
        
        return True
        
    except Exception as e:
        print(f"Error during merge: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_companies(output_dir: str = OUTPUT_DIR) -> None:
    """
    Merge analyses for all companies in the output directory.
    
    Args:
        output_dir: Path to output directory containing company folders
    """
    if not os.path.exists(output_dir):
        print(f"Output directory not found: {output_dir}")
        return
    
    print(f"\n{'='*60}")
    print(f"Merge Analysis - All Companies")
    print(f"Output directory: {output_dir}")
    print(f"{'='*60}\n")
    
    # Find all company directories
    company_dirs = []
    for item in os.listdir(output_dir):
        item_path = os.path.join(output_dir, item)
        if os.path.isdir(item_path):
            # Check if it has at least one analysis file
            if (os.path.exists(os.path.join(item_path, "deck_analysis.md")) or 
                os.path.exists(os.path.join(item_path, "web_analysis.md"))):
                company_dirs.append(item_path)
    
    if not company_dirs:
        print("No company directories with analysis files found")
        return
    
    print(f"Found {len(company_dirs)} companies to process\n")
    
    # Process each company
    success_count = 0
    for company_dir in company_dirs:
        if merge_company_analysis(company_dir):
            success_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Completed: {success_count}/{len(company_dirs)} companies")
    print(f"{'='*60}\n")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Process specific company directory
        company_dir = sys.argv[1]
        if not os.path.isabs(company_dir):
            company_dir = os.path.abspath(company_dir)
        
        merge_company_analysis(company_dir)
    else:
        # Process all companies
        run_all_companies()


if __name__ == "__main__":
    main()
