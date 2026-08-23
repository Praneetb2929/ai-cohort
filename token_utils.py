import tiktoken

def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """Calculate token count for a text string using tiktoken with a heuristic fallback."""
    if not text:
        return 0
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        # Fallback approximation (~4 chars per token)
        return max(1, len(text) // 4)

def estimate_cost(input_tokens: int, output_tokens: int, input_rate_per_1k: float = 0.00015, output_rate_per_1k: float = 0.0006) -> float:
    """Estimate total cost based on token consumption."""
    cost = (input_tokens / 1000.0 * input_rate_per_1k) + (output_tokens / 1000.0 * output_rate_per_1k)
    return round(cost, 6)