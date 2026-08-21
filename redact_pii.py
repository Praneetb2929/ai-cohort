import re

def redact_pii(text: str) -> str:
    """Redact names, member IDs, claim IDs, SSNs, phone numbers, and emails."""
    if not text:
        return ""
    # Member IDs (e.g., MEM-12345, mem_123, Member#98765)
    text = re.sub(r'(?i)\b(?:mem(?:ber)?[-_#\s]*)(\d+|[a-z0-9]+)\b', '[REDACTED_MEMBER_ID]', text)
    # Claim IDs (e.g., C-2031, CLAIM-9910)
    text = re.sub(r'(?i)\b(?:claim[-_#\s]*|c-)(\d+)\b', '[REDACTED_CLAIM_ID]', text)
    # Phone numbers
    text = re.sub(r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b', '[REDACTED_PHONE]', text)
    # Emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', '[REDACTED_EMAIL]', text)
    # Generic names following "member" or "patient"
    text = re.sub(r'(?i)\b(patient|member|user)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', r'\1 [REDACTED_NAME]', text)
    return text

if __name__ == "__main__":
    # Unit tests with 3 sample strings containing fake PHI/PII
    samples = [
        "Patient John Doe with member id MEM-94819 filed a claim.",
        "Status of claim C-2031 for contact john.doe@example.com is pending.",
        "Please call 555-123-4567 regarding member_id 88219."
    ]
    for s in samples:
        print(f"Original: {s}")
        print(f"Redacted: {redact_pii(s)}\n")