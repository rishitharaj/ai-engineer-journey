import os
from typing import List
from dataclasses import dataclass

@dataclass
class Document:
    content: str
    metadata: dict

def load_jobs(data_dir: str = "data/jobs") -> List[Document]:
    """Load all job posting text files from directory"""
    documents = []
    
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            documents.append(Document(
                content=content,
                metadata={
                    "filename": filename,
                    "filepath": filepath,
                    "source": "job_posting"
                }
            ))
    
    print(f"Loaded {len(documents)} documents")
    return documents


def chunk_documents(documents: List[Document], chunk_size: int = 500, overlap: int = 50) -> List[Document]:
    """Split documents into smaller chunks"""
    chunks = []
    
    for doc in documents:
        content = doc.content
        words = content.split()
        
        # slide a window of chunk_size words with overlap
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_content = " ".join(chunk_words)
            
            if len(chunk_content.strip()) > 50:  # skip tiny chunks
                chunks.append(Document(
                    content=chunk_content,
                    metadata={
                        **doc.metadata,
                        "chunk_index": i,
                    }
                ))
    
    print(f"Created {len(chunks)} chunks from {len(documents)} documents")
    return chunks