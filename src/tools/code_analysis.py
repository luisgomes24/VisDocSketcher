# Include Static code anaylis tools to be used by LLMs
import difflib
from pathlib import Path

from nbformat import read
from langchain_core.tools import tool
from typing import Annotated, Dict, Any, List
import ast


@tool
def get_diff(
    nb1: Annotated[Path, "Path to the first Jupyter notebook file."],
    nb2: Annotated[Path, "Path to the second Jupyter notebook file."],
) -> str:
    """Compares two notebooks and returns the differences as a string (similar to github)."""
    with open(nb1, "r") as f1:
        nb1 = read(f1, as_version=4)

    with open(nb2, "r") as f2:
        nb2 = read(f2, as_version=4)

    diff = difflib.unified_diff(
        [cell.source for cell in nb1.cells],
        [cell.source for cell in nb2.cells],
        fromfile=str(nb1),
        tofile=str(nb2),
    )
    return "".join(diff)


@tool
def build_dataflow_graph_ast(
    file_path: Annotated[str, "Path to Python file."],
) -> Dict[str, Any]:
    """Build a simplified dataflow graph showing data dependencies."""
    deps = extract_variable_dependencies(file_path)
    return {"dataflow_graph": deps}


@tool
def extract_variable_dependencies(
    file_path: Annotated[str, "Path to the Python file."],
) -> Dict[str, List[str]]:
    """Map variable assignments to variables or functions they depend on."""

    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    dependencies = {}

    class DependencyVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_target = None

        def visit_Assign(self, node):
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if targets:
                self.current_target = targets[0]
                deps = set()
                self.generic_visit(node.value)
                if self.current_target:
                    dependencies[self.current_target] = list(deps)
                self.current_target = None

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load) and self.current_target:
                dependencies.setdefault(self.current_target, []).append(node.id)

    DependencyVisitor().visit(tree)
    return dependencies
