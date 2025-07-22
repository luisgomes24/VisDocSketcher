from langgraph.graph import StateGraph
from typing import Callable, Any, Dict


def test_single_agent_workflow(
    agent_node_fn: Callable[[Dict], Dict],
    user_prompt: str,
    graph_name: str = "single_agent_graph",
) -> Dict[str, Any]:
    """
    Runs a simple single-agent LangGraph workflow with the given user prompt.

    Args:
        agent_node_fn (Callable): The function representing the agent node. It should accept a state dict and return an updated state dict.
        user_prompt (str): The input from the user to be processed by the agent.
        graph_name (str): Optional name of the graph.

    Returns:
        Dict: Final state after running the graph.
    """

    # Define the state type
    StateType = Dict[str, Any]

    # Create a graph with one agent node
    builder = StateGraph(StateType)
    builder.add_node("agent", agent_node_fn)
    builder.set_entry_point("agent")
    builder.set_finish_point("agent")

    graph = builder.compile(name=graph_name)

    # Run the graph with initial input
    initial_state = {"user_prompt": user_prompt}
    final_state = graph.invoke(initial_state)

    return final_state


from langgraph.graph import StateGraph, END, START
from typing import Callable, Dict, Any, Type


def test_single_agent_stream(
    agent_node_fn: Callable,
    state_class: Type,
    user_prompt: str,
    pretty_printer: Callable[[Dict[str, Any]], None] = None,
    graph_name: str = "single_agent_test",
):
    """
    Test a single-agent LangGraph with streaming output.

    Args:
        agent_node_fn (Callable): The agent node function.
        state_class (Type): The LangGraph state class, e.g., MessagesState.
        user_prompt (str): User message to test.
        pretty_printer (Callable): Optional function to print each chunk.
        graph_name (str): Optional graph name.

    Returns:
        final state dict
    """

    # Build graph with just one node
    graph = (
        StateGraph(state_class)
        .add_node("agent", agent_node_fn, destinations=(END,))
        .add_edge(START, "agent")
        .compile()
    )

    # Prepare initial state
    initial_state = {"messages": [{"role": "user", "content": user_prompt}]}

    # Stream execution
    final_chunk = None
    for chunk in graph.stream(initial_state):
        if pretty_printer:
            pretty_printer(chunk, last_message=True)
        final_chunk = chunk

    return final_chunk["agent"]
