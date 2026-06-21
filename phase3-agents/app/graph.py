from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.nodes import search_node, analyse_node, draft_node


def build_agent_graph():
    """Builds and compiles the recruiting agent graph"""

    graph = StateGraph(AgentState)

    # add nodes
    graph.add_node("search", search_node)
    graph.add_node("analyse", analyse_node)
    graph.add_node("draft", draft_node)

    # define the flow: search → analyse → draft → end
    graph.set_entry_point("search")
    graph.add_edge("search", "analyse")
    graph.add_edge("analyse", "draft")
    graph.add_edge("draft", END)

    return graph.compile()


# compile once at module level so it's reused across requests
agent_graph = build_agent_graph()