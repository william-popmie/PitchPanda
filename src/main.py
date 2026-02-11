"""
Main orchestrator for PitchPanda analysis.

Analyzes both web presence and pitch decks for startups listed in pitches.csv.
Creates a folder per company with web_analysis.md, deck_analysis.md, merged_analysis.md, and evaluation.md.

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

from .merge_analysis.graph import merge_graph, MergeState
from .merge_analysis.renderer import render_markdown as render_merged_markdown
from .merge_analysis.schemas import MergedAnalysis

from .evaluation.graph import evaluation_graph, EvaluationState
from .evaluation.renderer import render_evaluation
from .evaluation.schemas import CompanyEvaluation

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
        print(f"Running web analysis...")
        
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
        
        print(f"Web analysis saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Web analysis failed: {e}")
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
        print(f"Running deck analysis on: {Path(pdf_path).name}")
        
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
            
            print(f"Deck analysis saved to: {output_path}")
            return True
        else:
            print(f"Deck analysis failed - no result")
            return False
            
    except Exception as e:
        print(f"Deck analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_merge_analysis(company_name: str, output_dir: str) -> bool:
    """
    Run merge analysis combining deck and web analysis.
    
    Args:
        company_name: Name of the company
        output_dir: Directory containing deck_analysis.md and web_analysis.md
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"Running merge analysis...")
        
        # Check for input files
        deck_path = os.path.join(output_dir, "deck_analysis.md")
        web_path = os.path.join(output_dir, "web_analysis.md")
        
        deck_exists = os.path.exists(deck_path)
        web_exists = os.path.exists(web_path)
        
        if not deck_exists and not web_exists:
            print(f"No analysis files found to merge")
            return False
        
        # Create initial state
        state = MergeState(
            company_name=company_name,
            deck_analysis_path=deck_path if deck_exists else None,
            web_analysis_path=web_path if web_exists else None,
        )
        
        # Run the merge graph
        result = merge_graph.invoke(state)
        
        # Extract the merged analysis
        if isinstance(result, dict):
            merged_data = result.get("merged_analysis")
        else:
            merged_data = result.merged_analysis
        
        if not merged_data:
            print("Merge analysis failed - no result")
            return False
        
        # Convert to schema object
        merged_analysis = MergedAnalysis(**merged_data)
        
        # Render to markdown
        md_content = render_merged_markdown(merged_analysis)
        
        # Save to output directory
        output_path = os.path.join(output_dir, "merged_analysis.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"Merged analysis saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Merge analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_evaluation(company_name: str, output_dir: str) -> bool:
    """
    Run evaluation scoring based on merged analysis.
    
    Args:
        company_name: Name of the company
        output_dir: Directory containing merged_analysis.md
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"Running investment evaluation...")
        
        # Check for merged analysis
        merged_path = os.path.join(output_dir, "merged_analysis.md")
        
        if not os.path.exists(merged_path):
            print(f"No merged analysis found to evaluate")
            return False
        
        # Create initial state
        state = EvaluationState(
            company_name=company_name,
            merged_analysis_path=merged_path,
        )
        
        # Run the evaluation graph
        result = evaluation_graph.invoke(state)
        
        # Extract the evaluation
        if isinstance(result, dict):
            evaluation_data = result.get("evaluation")
        else:
            evaluation_data = result.evaluation
        
        if not evaluation_data:
            print("Evaluation failed - no result")
            return False
        
        # Convert to schema object
        evaluation = CompanyEvaluation(**evaluation_data)
        
        # Render to markdown
        md_content = render_evaluation(evaluation)
        
        # Save to output directory
        output_path = os.path.join(output_dir, "evaluation.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"Evaluation saved to: {output_path}")
        print(f"Score: {evaluation.overall_score:.1f}/5.0")
        return True
        
    except Exception as e:
        print(f"Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def analyze_company(company_name: str, company_url: str, csv_path: str = INPUT_CSV):
    """
    Run complete analysis pipeline for a company.
    
    Args:
        company_name: Name of the company
        company_url: URL of the company website
        csv_path: Path to the CSV file (used to locate decks directory)
    """
    print(f"\n{'='*60}")
    print(f"Analyzing: {company_name}")
    print(f"{'='*60}")
    
    # Create company-specific output directory
    company_slug = slugify(company_name)
    company_output_dir = os.path.join(OUTPUT_DIR, company_slug)
    ensure_dir(company_output_dir)
    
    # Track success
    web_success = False
    deck_success = False
    merge_success = False
    eval_success = False
    
    # Run web analysis
    if company_url:
        web_success = run_web_analysis(company_name, company_url, company_output_dir)
    else:
        print(f"No URL provided - skipping web analysis")
    
    # Find and run deck analysis
    pdf_path = find_deck_pdf(company_name, INPUT_DECKS_DIR)
    if pdf_path:
        deck_success = run_deck_analysis(company_name, pdf_path, company_output_dir)
    else:
        print(f"No PDF found for {company_name} - skipping deck analysis")
        print(f"Expected location: {INPUT_DECKS_DIR}/{company_slug}.pdf")
    
    # Run merge analysis if we have at least one analysis
    if web_success or deck_success:
        merge_success = run_merge_analysis(company_name, company_output_dir)
    
    # Run evaluation if merge was successful
    if merge_success:
        eval_success = run_evaluation(company_name, company_output_dir)
    
    # Summary
    print(f"\n Results saved to: {company_output_dir}")
    if web_success:
        print(f"web_analysis.md")
    if deck_success:
        print(f"deck_analysis.md")
    if merge_success:
        print(f"merged_analysis.md")
    if eval_success:
        print(f"evaluation.md")
    
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
            f"Missing input CSV at {csv_path}\n"
            f"Expected columns: startup_name,startup_url"
        )

    print(f"\n{'='*60}")
    print(f"PitchPanda - Complete Startup Analysis")
    print(f"{'='*60}")
    print(f"Reading from: {csv_path}")
    print(f"Output to: {OUTPUT_DIR}")
    print(f"\nPipeline: Web Analysis → Deck Analysis → Merge Analysis")
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
                print(f"Skipping row (missing company name): {row}")
                continue

            analyze_company(company_name, company_url, csv_path)
            companies_processed += 1

    print(f"\n{'='*60}")
    print(f"Complete Analysis Finished!")
    print(f"{'='*60}")
    print(f"Processed {companies_processed} companies")
    print(f"Results in: {OUTPUT_DIR}")
    print(f"\n Generated files per company:")
    print(f"-web_analysis.md - Web scraping & analysis")
    print(f"-deck_analysis.md - Pitch deck analysis")
    print(f"merged_analysis.md - Comprehensive overview")
    print(f"{'='*60}\n")


def main():
    """Main entry point."""
    csv_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_CSV
    run_all_companies(csv_path)


if __name__ == "__main__":
    main()
