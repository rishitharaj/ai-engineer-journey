import time
import json
import os
from datetime import datetime
from functools import wraps
from typing import Callable
from langfuse import get_client
from dotenv import load_dotenv

load_dotenv()

LOG_FILE = "logs/traces.jsonl"

# v4 SDK: get_client() reads credentials from env vars automatically
langfuse = get_client()

# Groq pricing (approx, per million tokens) — update if pricing changes
PRICING = {
    "llama-3.3-70b-versatile": {
        "input": 0.59,   # $ per 1M input tokens
        "output": 0.79   # $ per 1M output tokens
    }
}


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Rough cost estimate based on token counts"""
    rates = PRICING.get(model, {"input": 0.6, "output": 0.8})
    cost = (input_tokens / 1_000_000) * rates["input"] + \
           (output_tokens / 1_000_000) * rates["output"]
    return round(cost, 6)


def log_trace(trace: dict):
    """Append a trace entry to the JSON log file"""
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(trace) + "\n")


def traced_node(node_name: str):
    """Decorator that wraps a node function with timing + logging + Langfuse tracing"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(state, *args, **kwargs):
            start_time = time.time()
            timestamp = datetime.utcnow().isoformat()

            print(f"\n[TRACE] → Entering node: {node_name}")

            with langfuse.start_as_current_observation(as_type="span", name=node_name) as span:
                result_state = func(state, *args, **kwargs)

                latency_ms = round((time.time() - start_time) * 1000, 2)

                tokens_used = result_state.get("_last_tokens", 0)
                model = result_state.get("_last_model", "n/a")
                input_tokens = result_state.get("_last_input_tokens", 0)
                output_tokens = result_state.get("_last_output_tokens", 0)
                cost = estimate_cost(model, input_tokens, output_tokens)

                span.update(
                    output={"tokens_used": tokens_used, "model": model},
                    metadata={"latency_ms": latency_ms, "cost_usd": cost}
                )

            trace_entry = {
                "node": node_name,
                "timestamp": timestamp,
                "latency_ms": latency_ms,
                "tokens_used": tokens_used,
                "model": model,
                "cost_usd": cost
            }

            if "trace_log" not in result_state:
                result_state["trace_log"] = []
            result_state["trace_log"].append(trace_entry)

            print(f"[TRACE] ← Exiting node: {node_name} "
                  f"| {latency_ms}ms | {tokens_used} tokens "
                  f"| ${cost}")

            log_trace(trace_entry)

            return result_state
        return wrapper
    return decorator