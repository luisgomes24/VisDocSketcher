import logging

from tools.files import file_exists
from langgraph.graph import StateGraph, END, START
from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
from workflow.agents.analyser import create_analyser_agent
from workflow.agents.sketcher import create_sketcher_agent
from workflow.agents.repair import create_repair_agent
from workflow.agents.visuals import create_visuals_agent

# Set up logging
logger = logging.getLogger(__name__)

SUPERVISOR_PROMPT = """
You are a supervisor managing a diagram generation with the following agents.
For each agent you can pass the instructions and the necessary filepaths and saving directories.
They are capable of reading and writing files.
Each agent output must be saved in the corresponding saving directory.

1. Analyser Agent: 
    - Specialized in code analysis and understanding Jupyter notebooks.
    - You should give it the notebook file path and the saving directory.
    - It will return the path of the created report.
2. Sketcher Agent: 
    - Specialized in sketching Mermaid diagrams based on a report and the original code.
    - You should give it the report file path, the notebook file path and the saving directory.
    - It will return the path of the created diagram.
3. Repair Agent: 
    - Specialized in checking the validity and repairing Mermaid diagrams.
    - You should give it the mermaid diagram file path and the saving directory.
    - It will return the path of the repaired diagram if changes were made.
    - If no changes were made, you can continue the workflow with the previous diagram.
4. Visuals Agent: 
    - Specialized in enhancing Mermaid diagrams with visual elements and styling to make them more engaging and easier to understand. 
    - You should give it the mermaid diagram file path and the saving directory.
    - It will return the path of the enhanced diagram.

You MUST call the appropriate agents in the correct order:
To create a new diagram: call the Analyser Agent, then the Sketcher Agent, and the Visuals Agent afterwards.
To verify if an existing diagram is valid call the Repair Agent.
You must check if an agent output was saved correctly by using the file_exists tool.
If the file was not saved correctly, call the appropriate agent again.

Assign work to one agent at a time, do not call agents in parallel. 
Don't skip agents from each workflow.
Do not do any work yourself. 
"""


def create_workflow() -> StateGraph:
    """Create the workflow with the agents."""
    # Create agents
    analyser_agent = create_analyser_agent()
    sketcher_agent = create_sketcher_agent()
    repair_agent = create_repair_agent()
    visuals_agent = create_visuals_agent()

    workflow = create_supervisor(
        model=init_chat_model("openai:gpt-4o-mini"),
        agents=[
            analyser_agent,
            sketcher_agent,
            repair_agent,
            visuals_agent,
        ],
        prompt=(SUPERVISOR_PROMPT),
        add_handoff_back_messages=True,
        output_mode="last_message",
        tools=[file_exists],
    )

    return workflow.compile()
