from workflow.agents.analyser import create_analyser_agent
from workflow.agents.test_agent import test_single_agent_stream
from helpers.messages import pretty_print_messages
from langgraph.graph import MessagesState


def main():
    notebook_path = sys.argv[1]
    save_folder = sys.argv[2]
    if len(sys.argv) < 3:
        print("Usage: python test_analyser_agent.py <notebook_path> <save_folder>")
        sys.exit(1)

    user_prompt = f"""
    Analyze the notebook {notebook_path} to generate a report. 
    The report should be saved in the {save_folder} folder.
    """

    result = test_single_agent_stream(
        create_analyser_agent(),
        MessagesState,
        user_prompt=user_prompt,
        pretty_printer=pretty_print_messages,
    )

    print(result)


if __name__ == "__main__":
    main()
