from langchain_core.tools import tool

from typing import Annotated
import nbformat
from difflib import unified_diff
import logging
import os

logger = logging.getLogger(__name__)


@tool
def diff_notebook_code_cells(
    path1: Annotated[str, "Path to the first Jupyter notebook file."],
    path2: Annotated[str, "Path to the second Jupyter notebook file."],
) -> str:
    """Compute the differences between two Jupyter notebooks and return it as a string (similar to github)."""
    logger.info(f"** Calling diff_notebook_code_cells with {path1} and {path2} **")

    def get_code_cells(nb):
        return [cell["source"] for cell in nb.cells if cell["cell_type"] == "code"]

    # Load notebooks
    nb1 = nbformat.read(path1, as_version=4)
    nb2 = nbformat.read(path2, as_version=4)

    # Extract code cells
    code1 = get_code_cells(nb1)
    code2 = get_code_cells(nb2)

    # Compute diffs
    diffs = {"added": [], "removed": [], "changed": []}

    max_len = max(len(code1), len(code2))
    for i in range(max_len):
        if i >= len(code1):
            diffs["added"].append({"index": i, "source": code2[i]})
        elif i >= len(code2):
            diffs["removed"].append({"index": i, "source": code1[i]})
        elif code1[i] != code2[i]:
            diff_lines = list(
                unified_diff(
                    code1[i].splitlines(keepends=True),
                    code2[i].splitlines(keepends=True),
                    fromfile=f"cell_{i}_old",
                    tofile=f"cell_{i}_new",
                    lineterm="",
                )
            )
            diffs["changed"].append(
                {
                    "index": i,
                    "diff": diff_lines,
                    "old_source": code1[i],
                    "new_source": code2[i],
                }
            )

    return diffs


@tool
def extract_notebook_cells(
    file_path: Annotated[str, "Path to the Jupyter notebook file."],
) -> str:
    """Extract the cells (markdown and code) from a Jupyter notebook without the outputs."""
    logger.info(f"** Calling extract_notebook_cells for {file_path} **")

    with open(file_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    cells_content = []
    for cell in notebook.cells:
        if cell.cell_type in ["markdown", "code"]:
            cells_content.append(
                f"## {cell.cell_type.capitalize()} Cell\n{cell.source}\n"
            )

    return "\n".join(cells_content)


@tool
def save_mermaid_diagram(
    mermaid_code: Annotated[str, "Mermaid code to be saved into the file."],
    file_name: Annotated[str, "File path to save the mermaid diagram."],
    agent_name: Annotated[str, "Name of the agent that is saving the diagram."],
) -> Annotated[str, "Path of the saved mermaid diagram file."]:
    """Save the given mermaid code as a diagram file."""
    file_name = os.path.splitext(file_name)[0] + f"_{agent_name}.mmd"
    logger.info(f"** Calling save_mermaid_diagram with {file_name}. **")

    with open(file_name, "w") as file:
        file.write(f"{mermaid_code}")
    return f"Mermaid diagram saved to {file_name}"


@tool
def read_file(
    file_name: Annotated[str, "File path to read the text from."],
) -> Annotated[str, "Content of the text file."]:
    """Read the content from a text file."""
    logger.info(f"** Calling read_file with {file_name} **")
    with open(file_name, "r") as file:
        return file.read()


@tool
def write_file(
    content: Annotated[str, "Content to be written to the file."],
    file_name: Annotated[str, "File path to write the content to."],
) -> Annotated[str, "Path of the written file."]:
    """Write the given content to a text file."""
    logger.info(f"** Calling write_text_file with {file_name}. **")
    with open(file_name, "w") as file:
        file.write(content)
    return f"Text file saved to {file_name}"


@tool
def save_json_report(
    content: Annotated[str, "JSON content to be written to the file."],
    reports_dir: Annotated[
        str, "Path to the directory where the JSON file will be saved."
    ],
    notebook_name: Annotated[
        str,
        "Name of the original Jupyter notebook file (filename only, without extension and path).",
    ],
) -> Annotated[str, "Path of the written file."]:
    """Write the given content to a JSON file."""
    file_name = os.path.join(reports_dir, notebook_name + "_report.json")
    logger.info(f"** Calling save_json_report with {file_name}. **")
    with open(file_name, "w") as file:
        json.dump(content, file)
    return f"JSON report saved to {file_name}"


@tool
def file_exists(
    file_name: Annotated[str, "File path to check for existence."],
) -> Annotated[bool, "Whether the file exists or not."]:
    """Check if a file exists."""
    logger.info(f"** Calling file_exists with {file_name} **")
    return os.path.isfile(file_name)
