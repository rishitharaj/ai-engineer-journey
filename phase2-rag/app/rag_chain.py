from groq import Groq
from app.retriever import search_jobs, format_context
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

RAG_SYSTEM_PROMPT = """You are an expert Job Market Intelligence assistant for India's tech industry.

You answer questions about tech jobs, required skills, and career advice using ONLY the job postings provided as context.

Rules:
- Base your answers strictly on the provided job postings
- Always mention which companies/roles you're referencing
- If the context doesn't contain enough information, say so honestly
- Be specific and actionable in your advice
- Format responses clearly with bullet points where relevant"""


def rag_query(user_question: str, n_results: int = 3) -> dict:
    """Full RAG pipeline: retrieve → augment → generate"""

    # Step 1: Retrieve relevant job postings
    matches = search_jobs(user_question, n_results=n_results)
    context = format_context(matches)

    # Step 2: Augment prompt with retrieved context
    augmented_prompt = f"""Here are relevant job postings from the database:

{context}

---

Based on the job postings above, please answer this question:
{user_question}"""

    # Step 3: Generate answer with LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": RAG_SYSTEM_PROMPT},
            {"role": "user", "content": augmented_prompt}
        ]
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": [m["metadata"]["filename"] for m in matches],
        "tokens_used": response.usage.total_tokens
    }