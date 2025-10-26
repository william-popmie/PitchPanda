"""
CSV utilities for reading startup information from Pitches.csv
"""
import csv
import os
from typing import List, Dict, Optional


def read_pitches_csv(csv_path: str = "input/Pitches.csv") -> List[Dict[str, str]]:
    """
    Read startup information from a CSV file.
    
    Args:
        csv_path: Path to the CSV file (default: input/Pitches.csv)
        
    Returns:
        List of dictionaries containing startup name and URL
        Each dict has keys: 'name', 'url'
        
    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        ValueError: If the CSV file is empty or malformed
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    startups = []
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        
        # Skip header if present (optional - adjust based on actual CSV format)
        # Uncomment the next line if your CSV has a header row
        # next(csv_reader, None)
        
        for row_num, row in enumerate(csv_reader, start=1):
            if len(row) < 2:
                print(f"Warning: Row {row_num} has fewer than 2 columns, skipping")
                continue
            
            name = row[0].strip()
            url = row[1].strip()
            
            if name and url:
                startups.append({
                    'name': name,
                    'url': url
                })
            else:
                print(f"Warning: Row {row_num} has empty name or URL, skipping")
    
    if not startups:
        raise ValueError("No valid startup entries found in CSV file")
    
    return startups


def get_startup_names(csv_path: str = "input/Pitches.csv") -> List[str]:
    """
    Get a list of startup names from the CSV file.
    
    Args:
        csv_path: Path to the CSV file (default: input/Pitches.csv)
        
    Returns:
        List of startup names
    """
    startups = read_pitches_csv(csv_path)
    return [startup['name'] for startup in startups]


def get_startup_urls(csv_path: str = "input/Pitches.csv") -> List[str]:
    """
    Get a list of startup URLs from the CSV file.
    
    Args:
        csv_path: Path to the CSV file (default: input/Pitches.csv)
        
    Returns:
        List of startup URLs
    """
    startups = read_pitches_csv(csv_path)
    return [startup['url'] for startup in startups]


def get_startup_by_name(name: str, csv_path: str = "input/Pitches.csv") -> Optional[Dict[str, str]]:
    """
    Get startup information by name.
    
    Args:
        name: Name of the startup to find
        csv_path: Path to the CSV file (default: input/Pitches.csv)
        
    Returns:
        Dictionary with startup name and URL, or None if not found
    """
    startups = read_pitches_csv(csv_path)
    for startup in startups:
        if startup['name'].lower() == name.lower():
            return startup
    return None


if __name__ == "__main__":
    # Example usage
    try:
        startups = read_pitches_csv()
        print(f"Found {len(startups)} startups:")
        for startup in startups:
            print(f"  - {startup['name']}: {startup['url']}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
