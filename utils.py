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


def normalize_url(url: str) -> str:
    """
    Normalize a URL by ensuring it has a protocol and removing trailing slashes.
    
    Args:
        url: The URL to normalize
        
    Returns:
        A normalized URL string
        
    Example:
        >>> normalize_url("www.example.com")
        'https://www.example.com'
        >>> normalize_url("https://www.example.com/")
        'https://www.example.com'
        >>> normalize_url("http://example.com/path/")
        'http://example.com/path'
    """
    url = url.strip()
    
    # Add https:// if no protocol is specified
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Remove trailing slash (but keep it if it's just the root domain)
    if url.endswith('/') and url.count('/') > 2:
        url = url.rstrip('/')
    elif url.endswith('/') and url.count('/') == 2:
        # Root domain like "https://example.com/" -> "https://example.com"
        url = url.rstrip('/')
    
    return url


def get_domain_from_url(url: str) -> str:
    """
    Extract the domain name from a URL.
    
    Args:
        url: The URL to extract domain from
        
    Returns:
        The domain name without protocol or path
        
    Example:
        >>> get_domain_from_url("https://www.example.com/path")
        'www.example.com'
        >>> get_domain_from_url("http://subdomain.example.co.uk")
        'subdomain.example.co.uk'
    """
    # Remove protocol
    domain = re.sub(r'^https?://', '', url)
    
    # Remove path (everything after first /)
    domain = domain.split('/')[0]
    
    # Remove port if present
    domain = domain.split(':')[0]
    
    return domain


if __name__ == "__main__":
    # Test slugify function
    print("Testing slugify function:")
    test_cases = [
        "Acme Corp",
        "TechStart.io",
        "InnovateLab 2024!",
        "Data & Flow",
        "CloudSync___Pro",
    ]
    for test in test_cases:
        print(f"  '{test}' -> '{slugify(test)}'")
    
    # Test normalize_url function
    print("\nTesting normalize_url function:")
    url_tests = [
        "www.example.com",
        "https://www.example.com/",
        "http://example.com/path/",
        "example.com",
        "https://subdomain.example.co.uk/page",
    ]
    for test in url_tests:
        print(f"  '{test}' -> '{normalize_url(test)}'")
    
    # Test get_domain_from_url function
    print("\nTesting get_domain_from_url function:")
    for test in url_tests:
        normalized = normalize_url(test)
        print(f"  '{normalized}' -> '{get_domain_from_url(normalized)}'")
