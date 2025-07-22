from langchain_core.tools import tool
from typing import Annotated, List, Optional
import os
import uuid
import random
import pandas as pd
import shutil
import matplotlib

shutil.rmtree(matplotlib.get_cachedir())
# Set the backend before importing pyplot

matplotlib.use("Agg")  # Use the 'Agg' backend which doesn't require GUI
import matplotlib.pyplot as plt
from pathlib import Path


@tool
def generate_plot_id() -> Annotated[str, "Random plot ID to save the plot"]:
    """
    Generates a random plot ID.
    """
    return uuid.uuid4().hex[:4]


@tool
def add_image_to_node(
    node: Annotated[str, "Mermaid node to have the image added."],
    image_path: Annotated[str, "Path to the image to be added."],
) -> Annotated[str, "The modified node with the added image."]:
    """
    Receives a mermaid node and a path to an image and add the image to that node,
    while maintaining the text of the node.
    """
    logger.info(f"** Calling add_image_to_node with {node} and {image_path} **")
    node_text = node.split("[")[0]
    logger.info(f"New node: {node_text}<img src='{image_path}' />")
    return f"{node_text}<img src='{image_path}' />"
