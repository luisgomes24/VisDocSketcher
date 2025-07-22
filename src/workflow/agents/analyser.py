import logging

from langgraph.prebuilt import create_react_agent
from tools.files import extract_notebook_cells, write_file
from tools.code_analysis import build_dataflow_graph_ast, extract_variable_dependencies

# from tools.code_analysis import build_dataflow_graph_ast, extract_variable_dependencies
from typing import Dict

AGENT_PROMPT = """
You are a code analysis expert tasked with summarizing the key components of a Jupyter Notebook used in a data science workflow.
Your output will be consumed by another agent that will generate a visual documentation diagram to help a new team member quickly understand the notebook.

Analyze the notebook code, and extract the following structured information:

1. Data Sources
List of all input files or data sources (e.g., CSV files)
Short description of what each contains (if inferable)

2. Data variables
List the important variables used in the notebook related to data
For each of them, include a short description of what it is.

3. Data Flow
For each variable (especially DataFrames), track:
How it was created (e.g., read_csv, merge)
Where it flows (used in model training, saved, or plotted)

4. Models
Which models are used (e.g., RandomForest, XGBoost, etc.)
Input features and target variables
Hyperparameters if applicable, such as layers and neurons in ANNs


Output Format:
Return the output in structured JSON format:
{
"data_sources": [ ... ],
"data_variables": [ ... ],
"data_flow": [ ... ],
"models": [ ... ],
}
Focus on clarity and summarizing all the information that would help someone unfamiliar with the code quickly grasp what it does.

FINAL ACTION:
Save the analysis to a report file with the same name as the notebook with .json extension.
Don't save any other files.
Answer saying the file was saved and provide the path.

"""

logger = logging.getLogger(__name__)


def create_analyser_agent():
    return create_react_agent(
        model="openai:gpt-4o-mini",
        tools=[
            extract_notebook_cells,
            write_file,
        ],
        prompt=AGENT_PROMPT,
        name="analyser_agent",
    )
