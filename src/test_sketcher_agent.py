from workflow.agents.sketcher import create_sketcher_agent
from workflow.agents.test_agent import test_single_agent_stream
from helpers.messages import pretty_print_messages
from langgraph.graph import MessagesState


def main():
    notebook_path = sys.argv[1]
    report_path = sys.argv[2]
    save_folder = sys.argv[3]
    if len(sys.argv) < 4:
        print(
            "Usage: python test_sketcher_agent.py <notebook_path> <report_path> <save_folder>"
        )
        sys.exit(1)

    user_prompt = f"""
    Build the Mermaid diagram corresponding to the notebook {notebook_path}. 
    You can use the report {report_path} to understand the code. 
    The diagram should be saved in the {save_folder} folder.
    """

    result = test_single_agent_stream(
        create_sketcher_agent(),
        MessagesState,
        user_prompt=user_prompt,
        pretty_printer=pretty_print_messages,
    )


if __name__ == "__main__":
    main()
