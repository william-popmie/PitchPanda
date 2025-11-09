#!/usr/bin/env python3
"""
Helper script to rename PDF files to match company names from pitches.csv.

Usage:
    python scripts/prepare_pdfs.py

This will:
1. Read company names from input/pitches.csv
2. List PDF files in input/decks/
3. Help you match and rename PDFs to the correct slug format
"""
import os
import csv
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from core.utils import slugify


def main():
    # Paths
    base_dir = Path(__file__).parent.parent
    csv_path = base_dir / "input" / "pitches.csv"
    decks_dir = base_dir / "input" / "decks"
    
    if not csv_path.exists():
        print(f"❌ CSV not found: {csv_path}")
        return
    
    if not decks_dir.exists():
        print(f"❌ Decks directory not found: {decks_dir}")
        return
    
    # Read company names
    companies = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames:
            reader.fieldnames = [
                (fn or "").lstrip("\ufeff").strip() 
                for fn in reader.fieldnames
            ]
        
        for row in reader:
            row = {
                (k or "").lstrip("\ufeff").strip(): (v or "").strip() 
                for k, v in row.items()
            }
            name = row.get("startup_name", "")
            if name:
                companies.append(name)
    
    # List PDF files
    pdf_files = list(decks_dir.glob("*.pdf"))
    
    print("\n" + "="*60)
    print("📋 Company Names from CSV")
    print("="*60)
    for i, name in enumerate(companies, 1):
        slug = slugify(name)
        expected_file = decks_dir / f"{slug}.pdf"
        status = "✅" if expected_file.exists() else "❌"
        print(f"{i}. {name}")
        print(f"   Expected: {slug}.pdf {status}")
    
    print("\n" + "="*60)
    print("📄 PDF Files in input/decks/")
    print("="*60)
    for pdf in pdf_files:
        print(f"- {pdf.name}")
    
    print("\n" + "="*60)
    print("🔧 Rename Suggestions")
    print("="*60)
    
    # Suggest renames
    for name in companies:
        slug = slugify(name)
        expected_file = decks_dir / f"{slug}.pdf"
        
        if not expected_file.exists():
            # Find potential matches
            matches = []
            for pdf in pdf_files:
                if slug in slugify(pdf.stem) or slugify(pdf.stem) in slug:
                    matches.append(pdf)
            
            if matches:
                print(f"\n'{name}' → {slug}.pdf")
                print(f"Potential matches:")
                for match in matches:
                    print(f"  - {match.name}")
                    print(f"    Rename with: mv '{match}' '{expected_file}'")
            else:
                print(f"\n'{name}' → {slug}.pdf")
                print(f"  ⚠️  No matching PDF found")
    
    print("\n" + "="*60)
    print("✅ Done!")
    print("="*60)
    print("\nTo rename a file, use:")
    print("  cd input/decks")
    print("  mv 'old-name.pdf' 'new-name.pdf'")
    print()


if __name__ == "__main__":
    main()
