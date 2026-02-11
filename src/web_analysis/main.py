"""
Main runner for web analysis.

Analyzes startup websites from a CSV file and generates detailed analysis reports.

Usage:
    python -m src.web_analysis.main
    
Or with a custom CSV path:
    python -m src.web_analysis.main path/to/pitches.csv
"""
import os
import sys
import csv

from .graph import analysis_graph, AnalysisState


# Default paths
INPUT_CSV = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "input", "pitches.csv")
)

OUTPUT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "output")
) 


def run_csv(csv_path: str = INPUT_CSV):
    """
    Run web analysis on all startups in the CSV file.
    
    Args:
        csv_path: Path to CSV file with columns: startup_name, startup_url
    """
    if not os.path.exists(csv_path):
        raise SystemExit(
            f"Missing input CSV at {csv_path}\n"
            f"Expected columns: startup_name,startup_url"
        )

    print(f"\n{'='*60}")
    print(f"Starting Web Analysis")
    print(f"Reading from: {csv_path}")
    print(f"{'='*60}\n")

    # Read with utf-8-sig to strip BOM if present
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # Normalize headers in case of BOM / stray spaces
        if reader.fieldnames:
            reader.fieldnames = [
                (fn or "").lstrip("\ufeff").strip() 
                for fn in reader.fieldnames
            ]

        startup_number = 1
        for row in reader:
            # Normalize keys coming from DictReader just in case
            row = {
                (k or "").lstrip("\ufeff").strip(): (v or "").strip() 
                for k, v in row.items()
            }

            name = row.get("startup_name", "")
            url = row.get("startup_url", "")
            
            if not name or not url:
                print(f"Skipping row (missing name/url): {row}")
                continue

            print(f"\n[{startup_number}] Analyzing: {name}")
            print(f"URL: {url}")
            
            state = AnalysisState(startup_name=name, startup_url=url)
            result = analysis_graph.invoke(state)
            
            # Save the analysis to output folder (numbered folder, single file inside)
            # Sanitize startup name for folder (keep alphanum and hyphens)
            import re
            safe_name = re.sub(r"[^a-z0-9-]", "", name.lower().replace(" ", "-"))
            folder_name = f"{startup_number}-{safe_name}"
            output_dir = os.path.join(OUTPUT_DIR, folder_name)
            os.makedirs(output_dir, exist_ok=True)

            # Single markdown file inside the numbered folder
            output_file = os.path.join(output_dir, "web_analysis.md")
            
            from .renderer import render_markdown
            from .schemas import Analysis
            analysis = Analysis(**result["result_json"])
            markdown = render_markdown(name, url, analysis)
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown)
            
            print(f"Saved to: {output_file}")
            startup_number += 1

    print(f"\n{'='*60}")
    print(f"Analysis complete!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    # Allow custom CSV path as command line argument
    csv_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_CSV
    run_csv(csv_path)
