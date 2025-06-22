import re

ILLEGAL_CHARS_PATTERN = re.compile(r'[^a-zA-z0-9-_]')

def sanitize_name(name: str) -> str:
    """
    Sanitize a string to be used as a filename.
    Remove illegal characters and replace spaces with underscores.
    
    Args:
        name (str): The string to sanitize.
    Returns:
        str: The sanitized string.
    """
    name = name.lower().replace(" ", "_")
    sanitized = ILLEGAL_CHARS_PATTERN.sub('', name)
    return sanitized

def get_hash(string: str) -> str:
    """
    Generate a hash for a given string.
    
    Args:
        string (str): The string to hash.
    Returns:
        str: The hexadecimal representation of the hash.
    """
    import hashlib
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def get_os_safe_name(name: str) -> str:
    """
    Generate an OS-safe name for a given string.
    This function sanitizes the name and appends a hash to ensure uniqueness.
    Args:
        name (str): The string to convert.
    Returns:
        str: The OS-safe name.
    """
    if not name:
        raise ValueError("Name cannot be empty")

    return f"{sanitize_name(name)}-{get_hash(name)}"
