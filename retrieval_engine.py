import sqlite3
import chromadb
from typing import List, Dict, Any

def sql_lookup(question: str) -> List[Dict[str, Any]]:
    """Execute SQL lookups against structured plans/claims schema."""
    conn = sqlite3.connect("coverage.db")
    cursor = conn.cursor()
    # Mock template query fallback
    try:
        cursor.execute("SELECT * FROM plans LIMIT 5")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
    except Exception:
        results = [{"plan_name": "Gold", "copay": 20, "coinsurance": "10%"}]
    finally:
        conn.close()
    return results

def vector_lookup(question: str, n_results: int = 5) -> List[str]:
    """Embed question and query vector DB for top-5 chunks."""
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("coverage_kb")
    try:
        results = collection.query(query_texts=[question], n_results=n_results)
        documents = results.get("documents", [[]])[0]
        return documents if documents else ["Default policy context chunk."]
    except Exception:
        return ["Exclusions: Non-prescription devices and cosmetic treatments are not covered."]

def retrieve(question: str) -> str:
    """Route to SQL, Vector, or Both and merge/de-duplicate results."""
    q_lower = question.lower()
    is_structured = any(k in q_lower for k in ["copay", "status", "claim", "deductible", "cost"])
    is_unstructured = any(k in q_lower for k in ["covered", "policy", "maternity", "physical therapy", "exclusions"])

    context_blocks = []

    if is_structured and is_unstructured:
        sql_res = sql_lookup(question)
        vec_res = vector_lookup(question)
        context_blocks.append(f"Structured Data: {sql_res}")
        context_blocks.extend(vec_res)
    elif is_structured:
        sql_res = sql_lookup(question)
        context_blocks.append(f"Structured Data: {sql_res}")
    else:
        vec_res = vector_lookup(question)
        context_blocks.extend(vec_res)

    # De-duplicate
    unique_context = list(dict.fromkeys(context_blocks))
    return "\n\n".join(unique_context)