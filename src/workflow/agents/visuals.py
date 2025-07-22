from langgraph.prebuilt import create_react_agent
from tools.files import read_file, write_file
from tools.mermaid import validate_mermaid_from_file
from tools.plots import add_image_to_node, generate_plot_id
from .test_agent import test_single_agent_workflow

VISUALS_PROMPT = """
You are a visualization expert, focused on Data Science workflows and ML Models.
Your task is to clean and enhance Mermaid diagrams with visual elements.
Keep the original structure and meaning of the diagram intact. Do not change the diagram's structure.

Your responsibilities are:
1. Decide which nodes would benefit from new visual elements
2. Use emojis that represent the content/purpose of nodes when adequate
3. Apply consistent and visually appealing styling to nodes and edge (COLOURS)
4. Modify the nodes to include dummy plots adding <img src='{image_path}' /> <br/> inside the node text without scaling.
(e.g. C --> D["<img src='path/to/plot.svg'/> <br/> Node Text"];)

IMPORTANT GUIDELINES:
- Apply consistent color schemes based on node types:
    - Data nodes: Light blue (#87CEEB) - HIGHLIGHT THEM
    - ML Model nodes: Light green (#C6F4D6)
    - Output nodes: Light yellow (#F2C464)
    - Plot nodes: Light red (#FFCDD2)
- Ensure the enhanced diagram is still valid Mermaid syntax
- Use <br/> to add line breaks

AVAILABLE ICONS in ../data/icons:
- database.svg : Represents a structured data source such as an SQL or NoSQL database.
- file.svg : Represents a general file data source, such as CSV, JSON, or Excel.
- table.svg : Represents a tabular data structure, such as a pandas DataFrame.
- column_split.svg : Used to indicate splitting or selecting columns (features) from a dataset.
- row_split.svg : Represents splitting rows, such as train-test split or filtering observations.
- brain.svg : Symbolizes a learning process or a neural network model in ML.
- image.svg : Denotes image data or an image input/output in a computer vision pipeline.

If you use icons, they MUST be scaled to 100px.
(e.g. C --> D["<img src='path/to/icon.svg' width=100 height=100/> <br/> Node Text"];)

AVAILABLE DUMMY PLOT TEMPLATES in ../data/dummy_plots:
├── barplot_template.svg
├── boxplot_template.svg
├── hist_template.svg
├── lineplot_template.svg
└── scatter_plot_template.svg

FINAL ACTION:
Save the Mermaid file with the same name in the saving directory with .mmd extension.
Answer providing the saving filepath.
"""


def create_visuals_agent():
    return create_react_agent(
        model="openai:gpt-4o-mini",
        tools=[
            read_file,
            write_file,
            validate_mermaid_from_file,
            add_image_to_node,
            generate_plot_id,
        ],
        prompt=VISUALS_PROMPT,
        name="visuals_agent",
    )


def get_visuals_view(state: "DiagramState") -> dict:
    """
    Returns only the data that the visuals agent needs to see.
    This ensures data isolation - the visuals agent only sees the diagram content.
    """
    return {
        "diagram_content": state.get("diagram_content"),
        "analysis": state.get("analysis", ""),
    }
