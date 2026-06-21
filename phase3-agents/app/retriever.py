import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict

# path to Phase 2's existing vector database
CHROMA_PATH = "../phase2-rag/chroma_db"
COLLECTION_NAME = "job_postings"

print("Loading embedding model for Phase 3 agent...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded!")

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)


def get_collection():
    """Connect to Phase 2's existing job_postings collection"""
    return chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )


def search_jobs(query: str, n_results: int = 3) -> List[Dict]:
    """Semantic search over Phase 2's job postings"""
    collection = get_collection()

    if collection.count() == 0:
        return []

    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(n_results, collection.count())
    )

    matches = []
    for i in range(len(results["documents"][0])):
        matches.append({
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return matches