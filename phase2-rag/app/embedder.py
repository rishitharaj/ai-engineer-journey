import chromadb
from sentence_transformers import SentenceTransformer
from app.ingestor import load_jobs, chunk_documents, Document
from typing import List

# Load the embedding model once at module level
print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded!")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")

def get_or_create_collection(collection_name: str = "job_postings"):
    """Get existing collection or create a new one"""
    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}  # cosine similarity for semantic search
    )
    return collection


def embed_and_store(chunks: List[Document], collection_name: str = "job_postings"):
    """Convert chunks to vectors and store in ChromaDB"""
    collection = get_or_create_collection(collection_name)

    # check if already populated
    existing = collection.count()
    if existing > 0:
        print(f"Collection already has {existing} chunks. Skipping embedding.")
        return collection

    print(f"Embedding {len(chunks)} chunks...")

    # generate embeddings for all chunks at once
    texts = [chunk.content for chunk in chunks]
    embeddings = embedding_model.encode(texts, show_progress_bar=True)

    # store in ChromaDB
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=[chunk.metadata for chunk in chunks]
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB!")
    return collection


def initialise_vector_store():
    """Full pipeline: load → chunk → embed → store"""
    docs = load_jobs()
    chunks = chunk_documents(docs)
    collection = embed_and_store(chunks)
    return collection