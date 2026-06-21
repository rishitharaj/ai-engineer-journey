import time
import json
import os
from datetime import datetime
from functools import wraps
from typing import Callable

LOG_FILE = "logs/traces.jsonl"

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
    """Decorator that wraps a node function with timing + logging"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(state, *args, **kwargs):
            start_time = time.time()
            timestamp = datetime.utcnow().isoformat()

            print(f"\n[TRACE] → Entering node: {node_name}")

            result_state = func(state, *args, **kwargs)

            latency_ms = round((time.time() - start_time) * 1000, 2)

            trace_entry = {
                "node": node_name,
                "timestamp": timestamp,
                "latency_ms": latency_ms,
                "tokens_used": result_state.get("_last_tokens", 0),
                "model": result_state.get("_last_model", "n/a"),
                "cost_usd": estimate_cost(
                    result_state.get("_last_model", "llama-3.3-70b-versatile"),
                    result_state.get("_last_input_tokens", 0),
                    result_state.get("_last_output_tokens", 0)
                )
            }

            # accumulate trace history inside state
            if "trace_log" not in result_state:
                result_state["trace_log"] = []
            result_state["trace_log"].append(trace_entry)

            print(f"[TRACE] ← Exiting node: {node_name} "
                  f"| {latency_ms}ms | {trace_entry['tokens_used']} tokens "
                  f"| ${trace_entry['cost_usd']}")

            log_trace(trace_entry)

            return result_state
        return wrapper
    return decorator