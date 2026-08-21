import re
from redact_pii import redact_pii

# Input injection / adversarial patterns
INJECTION_PATTERNS = [
    r"(?i)ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"(?i)show\s+me\s+another\s+member('s)?\s+claims?",
    r"(?i)you\s+are\s+now\s+in\s+dan\s+mode",
    r"(?i)system\s*override",
    r"(?i)reveal\s+all\s+(passwords|api\s+keys|database\s+records)"
]

MEDICAL_ADVICE_PATTERNS = [
    r"(?i)\byou\s+should\s+take\b",
    r"(?i)\byour\s+condition\s+is\b",
    r"(?i)\bi\s+diagnose\s+you\s+with\b",
    r"(?i)\btake\s+\d+\s*mg\b"
]

def check_input_guardrail(prompt: str) -> bool:
    """Returns True if input prompt is safe, False if injection or unauthorized access is detected."""
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, prompt):
            return False
    return True

def apply_output_guardrail(response_text: str) -> str:
    """Scans for PHI/PII leakage, blocks medical advice, and appends provider disclaimer."""
    # Redact PHI/PII
    sanitized = redact_pii(response_text)
    
    # Flag medical advice and redirect
    for pattern in MEDICAL_ADVICE_PATTERNS:
        if re.search(pattern, sanitized):
            return (
                "I cannot provide medical diagnosis or treatment instructions. "
                "Please consult a licensed healthcare provider for clinical guidance. "
                "This is not medical advice."
            )
            
    if "not medical advice" not in sanitized.lower():
        sanitized += " This is not medical advice."
        
    return sanitized