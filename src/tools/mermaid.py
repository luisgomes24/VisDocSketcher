from langchain_core.tools import tool
import os
import subprocess
from typing import Annotated
import logging

logger = logging.getLogger(__name__)


@tool
def validate_mermaid_from_file(
    file_path: Annotated[str, "Path to file containing Mermaid diagram code"],
) -> Annotated[tuple[bool, str], "Tuple containing (is_valid: bool, errors: str)"]:
    """
    Validate Mermaid diagram file using local mermaid-cli.

    Args:
        file_path: Path to file containing Mermaid diagram code

    Returns:
        tuple: (is_valid: bool, errors: str)
    """

    logger.info(f"** Calling validate_mermaid_from_file with {file_path} **")

    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"

    try:
        result = subprocess.run(
            ["mmdc", "-i", file_path],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            return True, ""
        return False, clean_mermaid_error(result.stderr)

    except FileNotFoundError:
        return (
            False,
            "mermaid-cli (mmdc) not found. Please install with: npm install -g @mermaid-js/mermaid-cli",
        )
    except Exception as e:
        return False, str(e)


def clean_mermaid_error(full_error: str) -> str:
    """Extract just the first 4 lines of error messages"""
    if not full_error:
        return ""

    lines = full_error.splitlines()
    return "\n".join(lines[:5]).strip()
