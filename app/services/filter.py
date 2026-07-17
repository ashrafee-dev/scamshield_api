import re

def filter_sensitive(text :str) -> str:

# Email addresses
    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "[EMAIL]",
        text,
    )

# Phone numbers
    text = re.sub(
        r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b",
        "[PHONE]",
        text,
    )

# Credit card numbers
    text = re.sub(
        r"\b(?:\d[ -]*?){13,19}\b",
        "[CARD]",
        text,
    )

# SSN (US)
    text = re.sub(
        r"\b\d{3}-\d{2}-\d{4}\b",
        "[SSN]",
        text,
    )

# Long digit sequences (account numbers, IDs, etc.)
    text = re.sub(
        r"\b\d{5,}\b",
        "[NUMBER]",
        text,
    )

    return text
