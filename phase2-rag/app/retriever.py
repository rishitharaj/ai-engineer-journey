from app.embedder import embedding_model, get_or_create_collection
from typing import List, Dict

def search_jobs(query: str, n_results: int = 3) -> List[Dict]:
    """Search job postings semantically"""
    collection = get_or_create_collection()

    # convert query to vector
    query_embedding = embedding_model.encode([query]).tolist()

    # search ChromaDB for similar vectors
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(n_results, collection.count())
    )

    # format results
    matches = []
    for i in range(len(results["documents"][0])):
        matches.append({
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return matches


def format_context(matches: List[Dict]) -> str:
    """Format retrieved chunks into a context string for the LLM"""
    context_parts = []

    for i, match in enumerate(matches):
        source = match["metadata"].get("filename", "unknown")
        context_parts.append(
            f"[Job Posting {i+1} — {source}]\n{match['content']}"
        )

    return "\n\n---\n\n".join(context_parts)