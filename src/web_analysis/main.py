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
    print(f"🌐 Starting Web Analysis")
    print(f"📄 Reading from: {csv_path}")
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

        for row in reader:
            # Normalize keys coming from DictReader just in case
            row = {
                (k or "").lstrip("\ufeff").strip(): (v or "").strip() 
                for k, v in row.items()
            }

            name = row.get("startup_name", "")
            url = row.get("startup_url", "")
            
            if not name or not url:
                print(f"⚠️  Skipping row (missing name/url): {row}")
                continue

            print(f"\n🔍 Analyzing: {name}")
            print(f"🔗 URL: {url}")
            
            state = AnalysisState(startup_name=name, startup_url=url)
            analysis_graph.invoke(state)

    print(f"\n{'='*60}")
    print(f"✅ Analysis complete!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    # Allow custom CSV path as command line argument
    csv_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_CSV
    run_csv(csv_path)
