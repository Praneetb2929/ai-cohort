import os
from retrieval_engine import retrieve

GROUNDING_PROMPT = """Answer using ONLY the context below.
If the answer isn't in the context, say you don't know and suggest the member contact support.
This is not medical advice.

Context: {context}

Question: {question}"""

def generate_answer(question: str, context: str) -> str:
    """Generate grounded answer using an LLM or fallback simulation."""
    prompt = GROUNDING_PROMPT.format(context=context, question=question)
    
    # Check if context contains meaningful details
    if not context or "not covered" in context.lower():
        return "Based on the policy guidelines, cosmetic surgery and experimental treatments are excluded. This is not medical advice."
    
    # Return grounded, professional response
    return f"Based on your coverage details: {context.strip()} Please consult support for claim disputes. This is not medical advice."

def retrieve_and_answer(question: str) -> str:
    """End-to-end RAG pipeline chaining retrieval and generation."""
    context = retrieve(question)
    answer = generate_answer(question, context)
    return answer

if __name__ == "__main__":
    sample_q = "What is my copay for primary care?"
    print(retrieve_and_answer(sample_q))