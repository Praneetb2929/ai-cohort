# Vector Database Evaluation: Chroma vs. Pinecone

## Comparison

| Feature | Chroma | Pinecone |
| :--- | :--- | :--- |
| **Deployment (Local vs. Cloud)** | Embedded / Local (In-memory or persistent SQLite/Parquet file) | Fully Managed Cloud Service |
| **Free-Tier Limits** | 100% Free and Open Source (No tier limitations) | Limited free tier (1 index, fixed capacity/pod limits) |
| **Latency** | Ultra-low local latency (Direct process calls, no network roundtrip) | Network-dependent latency (API calls over HTTP/gRPC) |
| **Ease of Setup** | Minimal setup (`pip install chromadb`, instant local database) | Requires API keys, environment setup, and index configuration |
| **Access Control** | Metadata filtering applied per query in app logic | Metadata filtering with namespace isolation and IAM roles |

## Enterprise Access Control

In a production enterprise deployment handling multi-tenant healthcare or insurance data:
* **Chroma**: Per-member and per-plan access control relies on rigorous query-level metadata filtering (e.g., `where={"plan_type": "Gold"}`) alongside custom API middleware enforcement.
* **Pinecone**: Access control leverages isolated namespaces per plan/tenant and integrated cloud IAM policies combined with metadata filter criteria.

## Selected Vector Database Recommendation

Chroma is chosen going forward because it is fully open-source, runs natively without API costs or quotas, and allows zero-latency embedded persistence during development and testing.