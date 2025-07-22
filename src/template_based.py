import os
import time
import json
import csv
import re
from tqdm import tqdm


def generate_diagrams(notebooks_dir, diagrams_dir):
    """Generates mermaid diagrams from Jupyter notebooks using a regex-based constant template baseline."""
    processing_times = []

    for root, _, files in os.walk(notebooks_dir):
        for file in tqdm(files):
            if file.endswith(".ipynb"):
                notebook_path = os.path.join(root, file)
                start_time = time.time()
                diagram_path = os.path.join(diagrams_dir, f"{file.split('.')[0]}.mmd")

                if not os.path.exists(diagram_path):
                    try:
                        print(f"Generating diagram for {notebook_path}")
                        response = generate_diagram_from_notebook(notebook_path)
                        with open(diagram_path, "w") as f:
                            f.write(response)
                    except FileNotFoundError:
                        print(f"File not found: {file}")
                        continue
                    except Exception as e:
                        print(f"Error processing {file}: {e}")
                        continue
                    time.sleep(1)
                else:
                    print(f"Diagram already exists for {file}")

                duration = time.time() - start_time
                processing_times.append((file, round(duration, 2)))

    with open("processing_times_baseline.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename", "processing_time_seconds"])
        writer.writerows(processing_times)

    print("Saved processing times to processing_times_baseline.csv.")


def generate_diagram_from_notebook1(notebook_path):
    with open(notebook_path, "r") as f:
        notebook = json.load(f)

    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    code = "\n".join("".join(cell["source"]) for cell in code_cells)

    # Regex-based heuristics for pipeline stages
    stages = []

    if re.search(r"(read_csv|read_excel|open\(|load\(|pd\.read_|np\.load)", code):
        stages.append("DataLoad")

    if re.search(r"(dropna|fillna|merge|groupby|apply|map|replace)", code):
        stages.append("DataProcessing")

    if re.search(
        r"(fit|predict|train|LinearRegression|RandomForest|XGB|model\()", code
    ):
        stages.append("ModelTraining")

    if re.search(
        r"(accuracy_score|confusion_matrix|classification_report|mean_squared_error)",
        code,
    ):
        stages.append("Evaluation")

    # Add start/end nodes if missing
    if not stages:
        stages = ["Start", "SomeProcessing", "End"]
    else:
        if "DataLoad" not in stages:
            stages = ["Start"] + stages
        if "Evaluation" not in stages:
            stages.append("End")

    # Build Mermaid diagram
    diagram = "graph TD\n"
    for i in range(len(stages) - 1):
        diagram += f"    {stages[i]} --> {stages[i+1]}\n"

    # Add metadata for debugging
    diagram += f"\n%% Regex-based baseline: stages={stages}"

    return diagram


def generate_diagram_from_notebook2(notebook_path):
    with open(notebook_path, "r") as f:
        notebook = json.load(f)

    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    code = "\n".join("".join(cell["source"]) for cell in code_cells)

    # Heuristics for stages
    stages = []
    vars = {
        "data": None,
        "processed": None,
        "model": None,
        "preds": None,
    }

    # Try to find variable names using simple regex
    data_var = re.search(r"(\w+)\s*=\s*(pd\.read_csv|read_csv|np\.load|open\()", code)
    if data_var:
        vars["data"] = data_var.group(1)
        stages.append("DataLoad")

    clean_var = re.search(r"(\w+)\s*=\s*\1\.(dropna|fillna|replace|apply)", code)
    if clean_var:
        vars["processed"] = clean_var.group(1)
        stages.append("DataProcessing")

    model_var = re.search(
        r"(\w+)\s*=\s*(LinearRegression|RandomForest|XGB|.*Classifier|.*Regressor)",
        code,
    )
    if model_var:
        vars["model"] = model_var.group(1)
        stages.append("ModelTraining")

    predict_var = re.search(r"(\w+)\s*=\s*\w+\.predict\(", code)
    if predict_var:
        vars["preds"] = predict_var.group(1)
        stages.append("Prediction")

    if not stages:
        # Nothing matched, default diagram
        diagram = "graph TD\n"
        diagram += "    Start --> SomeProcessing --> End\n"
        diagram += "\n%% Regex-based fallback"
        return diagram

    # Build diagram
    diagram = "graph TD\n"
    if vars["data"]:
        diagram += f"    {vars['data']}[Raw Data] --> "
    else:
        diagram += f"    data[Raw Data] --> "

    if vars["processed"]:
        diagram += f"{vars['processed']}[Processed Data] --> "
    else:
        diagram += f"processed[Processed Data] --> "

    if vars["model"]:
        diagram += f"{vars['model']}[Model] --> "
    else:
        diagram += f"model[Model] --> "

    if vars["preds"]:
        diagram += f"{vars['preds']}[Predictions]\n"
    else:
        diagram += f"predictions[Predictions]\n"

    # Add some stylistic baseline metadata
    diagram += "\n%% Regex-based baseline with fake variable names"
    return diagram


def generate_diagram_from_notebook(notebook_path):
    with open(notebook_path, "r") as f:
        notebook = json.load(f)

    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    code = "\n".join("".join(cell["source"]) for cell in code_cells)

    # Initialize node variable names (defaults)
    vars = {
        "data": "raw_data",
        "processed": "processed_data",
        "model": "model",
        "preds": "predictions",
    }

    stages = []

    # Extract simple variable names using regex
    data_var = re.search(r"(\w+)\s*=\s*(pd\.read_csv|read_csv|np\.load|open\()", code)
    if data_var:
        vars["data"] = data_var.group(1)
        stages.append("DataLoad")

    clean_var = re.search(r"(\w+)\s*=\s*\1\.(dropna|fillna|replace|apply)", code)
    if clean_var:
        vars["processed"] = clean_var.group(1)
        stages.append("DataProcessing")

    model_var = re.search(
        r"(\w+)\s*=\s*(LinearRegression|RandomForest|XGB|.*Classifier|.*Regressor)",
        code,
    )
    if model_var:
        vars["model"] = model_var.group(1)
        stages.append("ModelTraining")

    predict_var = re.search(r"(\w+)\s*=\s*\w+\.predict\(", code)
    if predict_var:
        vars["preds"] = predict_var.group(1)
        stages.append("Prediction")

    if not stages:
        diagram = "graph TD\n"
        diagram += "    Start --> SomeProcessing --> End\n"
        diagram += "\n%% Regex-based fallback (no clear flow found)"
        return diagram

    # Mermaid-safe node labels
    def node(label, var):
        return f"{var}[{label}: {var}]"

    # Build diagram
    diagram = "graph TD\n"
    diagram += f"    {node('Raw Data', vars['data'])} --> "
    diagram += f"{node('Processed', vars['processed'])} --> "
    diagram += f"{node('Model', vars['model'])} --> "
    diagram += f"{node('Predictions', vars['preds'])}\n"

    diagram += f"\n%% Regex-based baseline with extracted variables: {vars}"
    return diagram


if __name__ == "__main__":
    notebooks_dir = sys.argv[1]
    diagrams_dir = sys.argv[2]
    if len(sys.argv) != 3:
        print("Usage: python template_based.py <notebooks_dir> <diagrams_dir>")
        sys.exit(1)
    os.makedirs(diagrams_dir, exist_ok=True)

    generate_diagrams(notebooks_dir, diagrams_dir)
