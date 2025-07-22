import json
import nbformat
from pathlib import Path

import json
import os

import re
import time
import PIL.Image
import os
import base64
import io
from PIL import Image
from tqdm import tqdm
import csv
import time

import openai

# NOTE: Change API Keys to run in .env file
# NOTE: Change to data directory ../data to absolute path in prompt

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """You are an expert software visualization system specialized in Python-based data science workflows. \
You will receive the full content of a Jupyter notebook and your task is to generate a high-level informal sketch of its structure. \
in the form of a Mermaid diagram. \
The diagram should use the Mermaid flowchart syntax and focus on representing major steps such as data loading, preprocessing, visualization, modeling, and evaluation. \
Use intuitive and include emojis in node labels (e.g. "📊 Barplot Results"). \
Use arrows to show the logical flow between steps, and only include meaningful, human-understandable operations. \
Omit boilerplate or trivial code such as import statements unless they are structurally relevant. \
Do not include any introductory or explanatory text in the output. \
Return only the Mermaid code block, without the placeholder ```mermaid and ```. \
The names of your nodes should be enclosed in double quotes (e.g. "Node Name"). \

You can include dummy plots and icons adding <img src='{image_path}' /> <br/> inside the node text.
(e.g. C --> D["<img src='path/to/plot.svg'/> <br/> Node Text"];)

AVAILABLE DUMMY PLOT TEMPLATES in ../data/dummy_plots:
├── barplot_template.svg
├── boxplot_template.svg
├── hist_template.svg
├── lineplot_template.svg
└── scatter_plot_template.svg
AVAILABLE ICONS in ../data/icons:
- database.svg : Represents a structured data source such as an SQL or NoSQL database.
- file.svg : Represents a general file data source, such as CSV, JSON, or Excel.
- table.svg : Represents a tabular data structure, such as a pandas DataFrame.
- column_split.svg : Used to indicate splitting or selecting columns (features) from a dataset.
- row_split.svg : Represents splitting rows, such as train-test split or filtering observations.
- brain.svg : Symbolizes a learning process or a neural network model in ML.
- image.svg : Denotes image data or an image input/output in a computer vision pipeline.

Here is the notebook content: \
"""


def is_notebook_empty(notebook_path):
    # Check if the file exists
    if not os.path.exists(notebook_path):
        raise FileNotFoundError(f"The file {notebook_path} does not exist.")

    # Open and read the notebook file
    with open(notebook_path, "r", encoding="utf-8") as nb_file:
        notebook_content = json.load(nb_file)

    # Check for cells in the notebook
    cells = notebook_content.get("cells", [])

    # If there are no cells, the notebook is considered empty
    if not cells:
        return True

    # Check each cell for content
    for cell in cells:
        if "source" in cell and cell["source"]:
            return False  # Non-empty cell found

    return True  # All cells are empty


class NotebookStep:
    def __init__(self, markdown, code):
        self.markdown = markdown
        self.code = code


def write_code_to_file(content, filepath):
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Content has been written to the file: {filepath}")


def change_file_extension(filepath, new_extension):
    path = Path(filepath)
    new_path = path.with_suffix(f".{new_extension}")
    return str(new_path)


def generate_notebook(steps_code, filepath):
    nb = nbformat.v4.new_notebook()
    nb["metadata"]["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb["metadata"]["language_info"] = {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.8.5",
    }

    for step in steps_code:
        nb["cells"].append(nbformat.v4.new_markdown_cell(step.markdown))
        nb["cells"].append(nbformat.v4.new_code_cell(step.code))

    with open(filepath, "w") as f:
        nbformat.write(nb, f)


def parse_notebook_steps(json_string):
    try:
        steps = json.loads(json_string)
        return [NotebookStep(step["markdown"], step["code"]) for step in steps]
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON string: {e}")
        return []


def extract_number(filename):
    """Extracts a number from a filename."""
    match = re.search(r"\d+", filename)
    if match:
        return int(match.group())
    else:
        return None


def generate_diagrams(notebooks_dir, diagrams_dir):
    """Generates notebooks for each image in the drawings directory."""
    processing_times = []
    for root, _, files in os.walk(notebooks_dir):
        for file in tqdm(files):
            if file.endswith(".ipynb"):
                print(f"Generating {file}.")
                notebook_path = os.path.join(root, file)
                start_time = time.time()
                diagram_path = os.path.join(diagrams_dir, f"{file.split('.')[0]}.mmd")
                if not os.path.exists(diagram_path):
                    try:
                        # Your image processing logic here
                        print(f"Generating {notebook_path}")
                        response = generate_diagram_from_notebook(notebook_path)
                        with open(diagram_path, "w") as f:
                            f.write(response)
                    except FileNotFoundError:
                        print(f"File not found: {file}")
                    except Exception as e:
                        print(f"Error processing image: {file}, Error: {e}")
                        continue
                    print(f"Waiting 1 seconds...")
                    time.sleep(1)
                else:
                    print(f"File {diagram_path} exists.")
                end_time = time.time()
                duration = end_time - start_time
                processing_times.append((file, round(duration, 2)))

    with open("processing_times.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename", "processing_time_seconds"])
        writer.writerows(processing_times)

    print("Saved processing times to processing_times.csv.")


def generate_diagram_from_notebook(notebook_path):
    with open(notebook_path, "r") as f:
        notebook_content = f.read()

    response = openai_client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_text",
                        "text": notebook_content,
                    },
                ],
            }
        ],
    )
    response = response.output_text

    return response


if __name__ == "__main__":

    notebooks_dir = sys.argv[1]
    diagrams_dir = sys.argv[2]
    if len(sys.argv) < 3:
        print("Usage: python single_agent.py <notebooks_dir> <diagrams_dir>")
        sys.exit(1)
    os.makedirs(diagrams_dir, exist_ok=True)
    generate_diagrams(notebooks_dir, diagrams_dir)
