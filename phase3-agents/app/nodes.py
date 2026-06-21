from groq import Groq
from app.retriever import search_jobs
from app.tracer import traced_node
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


@traced_node("search_similar_jobs")
def search_node(state):
    """Node 1: search Phase 2's job postings for similar roles"""
    query = state["job_description"]
    results = search_jobs(query, n_results=3)

    state["search_results"] = results
    # no LLM call here, so no tokens to log
    state["_last_tokens"] = 0
    state["_last_model"] = "n/a"
    state["_last_input_tokens"] = 0
    state["_last_output_tokens"] = 0

    return state


@traced_node("analyse_skill_requirements")
def analyse_node(state):
    """Node 2: LLM analyses common skill requirements across similar roles"""
    job_description = state["job_description"]
    search_results = state["search_results"]

    context = "\n\n---\n\n".join([r["content"] for r in search_results])

    prompt = f"""Here is a target job description:
{job_description}

Here are similar job postings found in our database:
{context}

Analyse the common technical and soft skill requirements across these postings.
List the top 5 most frequently required skills and note any patterns."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert technical recruiter analysing skill requirements."},
            {"role": "user", "content": prompt}
        ]
    )

    state["skill_analysis"] = response.choices[0].message.content
    state["_last_tokens"] = response.usage.total_tokens
    state["_last_model"] = MODEL
    state["_last_input_tokens"] = response.usage.prompt_tokens
    state["_last_output_tokens"] = response.usage.completion_tokens

    return state


@traced_node("generate_evaluation_rubric")
def draft_node(state):
    """Node 3: LLM generates a candidate evaluation rubric"""
    job_description = state["job_description"]
    skill_analysis = state["skill_analysis"]

    prompt = f"""Job description:
{job_description}

Skill analysis from similar roles:
{skill_analysis}

Create a structured candidate evaluation rubric with:
1. Must-have skills (with weight out of 100)
2. Nice-to-have skills (with weight out of 100)
3. 3 interview questions to assess the top skill gap areas"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert technical recruiter creating candidate evaluation rubrics."},
            {"role": "user", "content": prompt}
        ]
    )

    state["final_output"] = response.choices[0].message.content
    state["_last_tokens"] = response.usage.total_tokens
    state["_last_model"] = MODEL
    state["_last_input_tokens"] = response.usage.prompt_tokens
    state["_last_output_tokens"] = response.usage.completion_tokens

    return state