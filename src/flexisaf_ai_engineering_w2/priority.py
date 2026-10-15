"""Decision rules for urgency of a request. """

Urgent_Keywords = ("overheating", "fire", "burning", "shock", "sparks", "smoke", "swollen")

def has_urgent_keyword(issue: str) -> bool:
    """ Returns true if the issue text mentions a safety-related word."""
    text = issue.lower()
    return any(word in text for word in Urgent_Keywords)
    