from typing import Dict, Any

def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize input data to prevent injection attacks."""
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = value.strip()
        else:
            sanitized[key] = value
    return sanitized