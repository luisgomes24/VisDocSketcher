from workflow.agents.repair import create_repair_agent
from workflow.agents.test_agent import test_single_agent_stream
from helpers.messages import pretty_print_messages
from langgraph.graph import MessagesState


def main():
    mmd_file = sys.argv[1]
    save_folder = sys.argv[2]
    if len(sys.argv) < 3:
        print("Usage: python test_repair_agent.py <mmd_file> <save_folder>")
        sys.exit(1)

    user_prompt = f"""
    Repair the diagram {mmd_file} to fix any errors. 
    The repaired diagram should be saved in the {save_folder} folder.
    """

    result = test_single_agent_stream(
        create_repair_agent(),
        MessagesState,
        user_prompt=user_prompt,
        pretty_printer=pretty_print_messages,
    )


if __name__ == "__main__":
    main()
