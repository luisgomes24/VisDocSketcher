import logging
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List
from workflow.team import create_workflow
from helpers.setup import init_keys, setup_logging
from tqdm import tqdm
import time
import csv

# Initialize logger
logger = logging.getLogger(__name__)

# Base directories

# NOTE: Change to data directory

BASE_DIR = Path("../")
DATA_DIR = BASE_DIR / "data/distil1000"

NOTEBOOKS_DIR = DATA_DIR / "notebooks"
SKETCHER_DIR = DATA_DIR / "multi_agent_sketches"
REPAIR_DIR = DATA_DIR / "multi_agent_repairs"
VISUALS_DIR = DATA_DIR / "multi_agent_visuals"
REPORTS_DIR = DATA_DIR / "multi_agent_reports"


def get_notebooks(directory: str) -> List[Path]:
    """Get all .ipynb files in the specified directory."""
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Directory not found: {directory}")

    notebooks = list(path.glob("**/*.ipynb"))
    if not notebooks:
        logger.warning(f"No .ipynb files found in {directory}")
    return notebooks


def process_notebook(notebook_path: Path):
    """Process a single notebook and generate its diagram."""
    logger.info(f"Processing notebook: {notebook_path}")
    workflow = create_workflow()
    # Create output directories if they don't exist
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    SKETCHER_DIR.mkdir(parents=True, exist_ok=True)
    REPAIR_DIR.mkdir(parents=True, exist_ok=True)
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)

    # Process the notebook
    user_prompt = f"""
    Analyze the notebook {notebook_path} and generate a diagram of the workflow.
    The analysis should be saved in {REPORTS_DIR} path with the same name as the notebook.
    Diagrams sketches should be saved in {SKETCHER_DIR} path with the same name as the notebook. 
    Any repairs should be saved in {REPAIR_DIR} path with the same name as the notebook. 
    Diagrams with visuals should be saved in {VISUALS_DIR} path with the same name as the notebook. 
    """

    # Execute the workflow for this notebook
    try:
        for chunk in workflow.stream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ]
            }
        ):
            # if "messages" in chunk:
            #     pretty_print_messages(chunk["messages"])
            for node, output in chunk.items():
                for message in output["messages"]:
                    logger.info(f"Node: {node}: {message.content}")
        logger.info(f"Processed {notebook_path}")

    except Exception as e:
        logger.error(f"Error processing {notebook_path}: {str(e)}")


def has_any_matching_file(stem: str) -> bool:
    dirs = [REPORTS_DIR, SKETCHER_DIR, REPAIR_DIR, VISUALS_DIR]
    return any(any(p.stem == stem for p in d.glob("*")) for d in dirs)


def main():
    # Set up logging
    setup_logging()

    # Initialize environment and workflow
    init_keys()

    # Get input directory from user
    # input_dir = input("Enter the path to the directory containing notebooks: ").strip()
    input_dir = str(NOTEBOOKS_DIR)
    logger.info(f"Using default directory: {input_dir}")

    # Process notebooks in the directory
    # Get and filter notebooks
    notebooks = [
        nb for nb in get_notebooks(input_dir) if not has_any_matching_file(nb.stem)
    ]
    if not notebooks:
        logger.warning("No notebooks found in the directory.")
        return

    logger.info(f"Found {len(notebooks)} notebook(s) to process")

    processing_times = []
    for notebook in tqdm(notebooks):
        start_time = time.time()
        try:
            if not has_any_matching_file(notebook.stem):
                process_notebook(notebook)
            else:
                logger.info(f"Skipping {notebook}. Already processed.")
        except Exception as e:
            logger.error(f"Error processing {notebook}: {str(e)}")
            logger.info("Continuing to the next notebook...")
            continue
        end_time = time.time()
        duration = end_time - start_time
        processing_times.append((notebook, round(duration, 2)))
    else:
        logger.info(f"Skipping {notebook}. Already processed.")

    logger.info("\nAll notebooks processed successfully!")
    with open("processing_times_multi_agent.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename", "processing_time_seconds"])
        writer.writerows(processing_times)

    print("Saved processing times to processing_times_multi_agent.csv.")


if __name__ == "__main__":
    main()
