from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.graph import agent_graph
from app.tracer import langfuse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Recruiting Agent API",
    description="Multi-agent system for job analysis and candidate evaluation, with full observability",
    version="3.0.0"
)


class AgentRequest(BaseModel):
    job_description: str


class AgentResponse(BaseModel):
    final_output: str
    trace_log: list


@app.post("/api/v3/evaluate", response_model=AgentResponse)
async def evaluate(request: AgentRequest):
    try:
        result = agent_graph.invoke({
            "job_description": request.job_description
        })

        langfuse.flush()

        return AgentResponse(
            final_output=result["final_output"],
            trace_log=result["trace_log"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok", "version": "3.0.0", "component": "multi-agent recruiting pipeline"}