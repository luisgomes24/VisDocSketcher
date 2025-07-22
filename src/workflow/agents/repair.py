from langgraph.prebuilt import create_react_agent
from tools.files import read_file, write_file
from tools.mermaid import validate_mermaid_from_file

MERMAID_REPAIR_PROMPT = """
You are a Mermaid.js code check and repair expert. 
Your task is to analyze and fix issues in Mermaid.js diagram code while preserving its original functionality and intent.

One of the most common issues is the use of special characters in the node names. 
You should include double quotes in the node name. 
Example: X[A (great) node] SHOULD BE X["A (great) node"]

REQUIREMENTS:
1. Carefully analyze the provided Mermaid.js code for any syntax errors or issues
2. Fix any problems while maintaining the original diagram's structure and meaning
3. Make necessary changes to fix errors or improve the diagram's reliability
4. If the diagram is correct, answer saying no changes are needed.
5. Ensure all the node text is enclosed in double quotes ""

FINAL ACTION:
If the file is correct, answer saying no changes are needed.
Otherwise, save the repaired Mermaid.js file with the same name as the old mermaid file in the new path and provide the path.
"""


def create_repair_agent():
    return create_react_agent(
        model="openai:gpt-4o-mini",
        tools=[read_file, write_file, validate_mermaid_from_file],
        prompt=MERMAID_REPAIR_PROMPT,
        name="repair_agent",
    )
