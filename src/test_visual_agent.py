from workflow.agents.visuals import create_visuals_agent
from workflow.agents.test_agent import test_single_agent_stream
from helpers.messages import pretty_print_messages
from langgraph.graph import MessagesState


def main():

    mmd_file = sys.argv[1]
    save_folder = sys.argv[2]
    if len(sys.argv) < 3:
        print("Usage: python test_visual_agent.py <mmd_file> <save_folder>")
        sys.exit(1)

    user_prompt = f"""
    Enhance the diagram {mmd_file} with visual elements. 
    The enhanced diagram should be saved in the {save_folder} folder.
    """

    # result = test_single_agent_stream(
    #     agent_node_fn=create_visuals_agent(),
    #     user_prompt=user_prompt,
    #     graph_name="visuals_agent_graph",
    # )

    result = test_single_agent_stream(
        create_visuals_agent(),
        MessagesState,
        user_prompt=user_prompt,
        pretty_printer=pretty_print_messages,
    )


if __name__ == "__main__":
    main()
