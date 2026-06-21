from typing import TypedDict, List, Optional


class AgentState(TypedDict, total=False):
    # input
    job_description: str

    # search node output
    search_results: List[dict]

    # analyse node output
    skill_analysis: str

    # draft node output
    final_output: str

    # observability — populated by tracer.py
    trace_log: List[dict]
    _last_tokens: int
    _last_model: str
    _last_input_tokens: int
    _last_output_tokens: int