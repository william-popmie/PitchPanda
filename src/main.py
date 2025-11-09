"""
Main orchestrator for PitchPanda analysis.

Analyzes both web presence and pitch decks for startups listed in pitches.csv.
Creates a folder per company with web_analysis.md and deck_analysis.md.

Usage:
    python -m src.main
    
Or with a custom CSV path:
    python -m src.main path/to/pitches.csv
"""
import os
import sys
import csv
from pathlib import Path

from .web_analysis.graph import analysis_graph, AnalysisState
from .web_analysis.renderer import render_markdown
from .web_analysis.schemas import Analysis

from .deck_analysis.graph import deck_graph, DeckState
from .deck_analysis.renderer_updated import render_deck_markdown

from .core.utils import slugify, ensure_dir


# Default paths
INPUT_CSV = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "input", "pitches.csv")
)
INPUT_DECKS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "input", "decks")
)
OUTPUT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "output")
)


def find_deck_pdf(company_name: str, decks_dir: str) -> str | None:
    """
    Find a PDF file matching the company name.
    
    Args:
        company_name: Name of the company
        decks_dir: Directory containing PDF files
        
    Returns:
        Path to PDF file if found, None otherwise
    """
    # Try exact match first
    slug = slugify(company_name)
    exact_path = os.path.join(decks_dir, f"{slug}.pdf")
    if os.path.exists(exact_path):
        return exact_path
    
    # Try case-insensitive match
    if not os.path.exists(decks_dir):
        return None
        
    for file in Path(decks_dir).glob("*.pdf"):
        if slugify(file.stem) == slug:
            return str(file)
    
    # Try partial match (company name in filename)
    for file in Path(decks_dir).glob("*.pdf"):
        if slug in slugify(file.stem):
            return str(file)
    
    return None


def run_web_analysis(company_name: str, company_url: str, output_dir: str) -> bool:
    """
    Run web analysis for a company and save to output directory.
    
    Args:
        company_name: Name of the company
        company_url: URL of the company website
        output_dir: Directory to save the analysis
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"  🌐 Running web analysis...")
        
        # Run the analysis graph
        state = AnalysisState(startup_name=company_name, startup_url=company_url)
        result = analysis_graph.invoke(state)
        
        # Extract the analysis
        if isinstance(result, dict):
            analysis_data = result.get("result_json", {})
        else:
            analysis_data = result.result_json
        
        # Render to markdown
        analysis = Analysis(**analysis_data)
        md_content = render_markdown(company_name, company_url, analysis)
        
        # Save to output directory
        output_path = os.path.join(output_dir, "web_analysis.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"  ✅ Web analysis saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"  ❌ Web analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_deck_analysis(company_name: str, pdf_path: str, output_dir: str) -> bool:
    """
    Run pitch deck analysis for a company and save to output directory.
    
    Args:
        company_name: Name of the company
        pdf_path: Path to the PDF file
        output_dir: Directory to save the analysis
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"  🎯 Running deck analysis on: {Path(pdf_path).name}")
        
        # Create initial state
        state = DeckState(pdf_path=pdf_path)
        
        # Run the graph
        result = deck_graph.invoke(state)
        
        # Extract the analysis
        if isinstance(result, dict):
            final_analysis = result.get("final_analysis")
        else:
            final_analysis = result.final_analysis
        
        if final_analysis:
            # Render to markdown
            md_content = render_deck_markdown(final_analysis)
            
            # Save to output directory
            output_path = os.path.join(output_dir, "deck_analysis.md")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            
            print(f"  ✅ Deck analysis saved to: {output_path}")
            return True
        else:
            print(f"  ❌ Deck analysis failed - no result")
            return False
            
    except Exception as e:
        print(f"  ❌ Deck analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def analyze_company(company_name: str, company_url: str, csv_path: str = INPUT_CSV):
    """
    Run both web and deck analysis for a company.
    
    Args:
        company_name: Name of the company
        company_url: URL of the company website
        csv_path: Path to the CSV file (used to locate decks directory)
    """
    print(f"\n{'='*60}")
    print(f"📊 Analyzing: {company_name}")
    print(f"{'='*60}")
    
    # Create company-specific output directory
    company_slug = slugify(company_name)
    company_output_dir = os.path.join(OUTPUT_DIR, company_slug)
    ensure_dir(company_output_dir)
    
    # Track success
    web_success = False
    deck_success = False
    
    # Run web analysis
    if company_url:
        web_success = run_web_analysis(company_name, company_url, company_output_dir)
    else:
        print(f"  ⚠️  No URL provided - skipping web analysis")
    
    # Find and run deck analysis
    pdf_path = find_deck_pdf(company_name, INPUT_DECKS_DIR)
    if pdf_path:
        deck_success = run_deck_analysis(company_name, pdf_path, company_output_dir)
    else:
        print(f"  ⚠️  No PDF found for {company_name} - skipping deck analysis")
        print(f"      Expected location: {INPUT_DECKS_DIR}/{company_slug}.pdf")
    
    # Summary
    print(f"\n  📁 Results saved to: {company_output_dir}")
    if web_success:
        print(f"     ✓ web_analysis.md")
    if deck_success:
        print(f"     ✓ deck_analysis.md")
    
    if not web_success and not deck_success:
        print(f"  ⚠️  No analyses completed for {company_name}")


def run_all_companies(csv_path: str = INPUT_CSV):
    """
    Run analysis on all companies in the CSV file.
    
    Args:
        csv_path: Path to CSV file with columns: startup_name, startup_url
    """
    if not os.path.exists(csv_path):
        raise SystemExit(
            f"❌ Missing input CSV at {csv_path}\n"
            f"Expected columns: startup_name,startup_url"
        )

    print(f"\n{'='*60}")
    print(f"🚀 PitchPanda - Complete Startup Analysis")
    print(f"{'='*60}")
    print(f"📄 Reading from: {csv_path}")
    print(f"📁 Output to: {OUTPUT_DIR}")
    print(f"{'='*60}\n")

    # Read CSV and process each company
    companies_processed = 0
    
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # Normalize headers in case of BOM / stray spaces
        if reader.fieldnames:
            reader.fieldnames = [
                (fn or "").lstrip("\ufeff").strip() 
                for fn in reader.fieldnames
            ]

        for row in reader:
            # Normalize keys coming from DictReader just in case
            row = {
                (k or "").lstrip("\ufeff").strip(): (v or "").strip() 
                for k, v in row.items()
            }

            company_name = row.get("startup_name", "")
            company_url = row.get("startup_url", "")
            
            if not company_name:
                print(f"⚠️  Skipping row (missing company name): {row}")
                continue

            analyze_company(company_name, company_url, csv_path)
            companies_processed += 1

    print(f"\n{'='*60}")
    print(f"✅ Analysis complete!")
    print(f"📊 Processed {companies_processed} companies")
    print(f"📁 Results in: {OUTPUT_DIR}")
    print(f"{'='*60}\n")


def main():
    """Main entry point."""
    csv_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_CSV
    run_all_companies(csv_path)


if __name__ == "__main__":
    main()
