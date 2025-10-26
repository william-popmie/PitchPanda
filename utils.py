"""
General utility functions
"""
import re
import os


def slugify(text: str) -> str:
    """
    Convert a string to a URL-friendly slug.
    
    Args:
        text: The text to convert to a slug
        
    Returns:
        A lowercase, hyphenated slug string
        
    Example:
        >>> slugify("Acme Corp")
        'acme-corp'
        >>> slugify("TechStart.io 2024!")
        'techstart-io-2024'
    """
    # Convert to lowercase
    text = text.lower()
    
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    
    # Remove any characters that aren't alphanumeric or hyphens
    text = re.sub(r'[^\w\-]', '', text)
    
    # Replace multiple consecutive hyphens with a single hyphen
    text = re.sub(r'-+', '-', text)
    
    # Strip leading/trailing hyphens
    text = text.strip('-')
    
    return text


def ensure_directory_exists(directory: str) -> None:
    """
    Create a directory if it doesn't exist.
    
    Args:
        directory: Path to the directory to create
    """
    os.makedirs(directory, exist_ok=True)


if __name__ == "__main__":
    # Test slugify function
    test_cases = [
        "Acme Corp",
        "TechStart.io",
        "InnovateLab 2024!",
        "Data & Flow",
        "CloudSync___Pro",
    ]
    
    print("Testing slugify function:")
    for test in test_cases:
        print(f"  '{test}' -> '{slugify(test)}'")
