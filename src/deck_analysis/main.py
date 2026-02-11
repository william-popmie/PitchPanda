"""
Main runner for pitch deck analysis.

Usage:
    python -m src.deck_analysis.main input/decks/my_pitch.pdf
    
Or analyze all PDFs in input/decks/:
    python -m src.deck_analysis.main
"""
import os
import sys
from pathlib import Path

from .graph import deck_graph, DeckState
from .renderer_updated import render_deck_markdown
from ..core.utils import ensure_dir


# Paths
INPUT_DECKS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "input", "decks")
)
OUTPUT_DECKS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "output", "decks")
)


def analyze_deck(pdf_path: str) -> None:
    """
    Analyze a single pitch deck PDF.
    
    Args:
        pdf_path: Path to the PDF file
    """
    print(f"\n{'='*60}")
    print(f"🎯 Analyzing: {Path(pdf_path).name}")
    print(f"{'='*60}\n")
    
    # Create initial state
    state = DeckState(pdf_path=pdf_path)
    
    # Run the graph
    try:
        result = deck_graph.invoke(state)
        
        # LangGraph returns a dict, so access it like a dict
        final_analysis = result.get("final_analysis") if isinstance(result, dict) else result.final_analysis
        deck_name = result.get("deck_name") if isinstance(result, dict) else result.deck_name
        
        if final_analysis:
            # Render to markdown
            md_content = render_deck_markdown(final_analysis)
            
            # Save output
            ensure_dir(OUTPUT_DECKS_DIR)
            output_filename = f"{deck_name}_analysis.md"
            output_path = os.path.join(OUTPUT_DECKS_DIR, output_filename)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            
            print(f"\nAnalysis saved to: {output_path}")
            print(f"{'='*60}\n")
        else:
            print(f"\nAnalysis failed for {pdf_path}")
    
    except Exception as e:
        print(f"\nError analyzing {pdf_path}: {e}")
        import traceback
        traceback.print_exc()


def analyze_all_decks():
    """Analyze all PDF files in the input/decks directory."""
    if not os.path.exists(INPUT_DECKS_DIR):
        print(f"Input directory not found: {INPUT_DECKS_DIR}")
        print(f"Create it and add PDF files to analyze.")
        return
    
    # Find all PDF files
    pdf_files = list(Path(INPUT_DECKS_DIR).glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {INPUT_DECKS_DIR}")
        print(f"Add some pitch deck PDFs to analyze.")
        return
    
    print(f"\n🔍 Found {len(pdf_files)} PDF file(s) to analyze")
    
    for pdf_path in pdf_files:
        analyze_deck(str(pdf_path))


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Analyze specific file
        pdf_path = sys.argv[1]
        if not os.path.exists(pdf_path):
            print(f"File not found: {pdf_path}")
            sys.exit(1)
        analyze_deck(pdf_path)
    else:
        # Analyze all PDFs in input/decks/
        analyze_all_decks()


if __name__ == "__main__":
    main()
