# VisDocSketcher: Visual Document Generation

This project provides tools for generating visual representations of Jupyter notebooks using both single-agent and multi-agent approaches. The system is designed to help understand and visualize data science workflows in Python.

## Features

- **Single-Agent Mode**: A single AI agent generates visualizations of notebook workflows
- **Multi-Agent Mode**: Multiple specialized agents collaborate to analyze and visualize notebook structures
- **Mermaid Diagram Generation**: Produces flowcharts of notebook workflows
- **Intermediate Artifacts**: Generates both visual diagrams as an output and structured reports

## Prerequisites

- OpenAI API key
- LangChain API key (for multi-agent mode)
- Use `environment.yml` to create a conda environment

## Installation

1. Create and activate the conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate visdocsketcher_env
   ```

2. Set up your environment variables:
   - Open the `.env` file in the `src` directory
   - Add your API keys to the `.env` file

## Usage

### Single-Agent Mode

To generate visualizations using the single-agent approach:

```bash
python src/single_agent.py <path_to_notebooks_directory> <output_directory>
```

Example:
```bash
python src/single_agent.py data/notebooks data/output/single_agent
```

### Multi-Agent Mode

To use the multi-agent workflow:

```bash
python src/multi_agent.py
```

### Configuration

Modify the following paths in `src/multi_agent.py` according to your setup:

```python
BASE_DIR = Path("../")
DATA_DIR = BASE_DIR / "data/Distill1000"
NOTEBOOKS_DIR = DATA_DIR / "notebooks"
SKETCHER_DIR = DATA_DIR / "multi_agent_sketches"
REPAIR_DIR = DATA_DIR / "multi_agent_repairs"
VISUALS_DIR = DATA_DIR / "multi_agent_visuals"
REPORTS_DIR = DATA_DIR / "multi_agent_reports"
```

## Output

- **Single-Agent**: Generates Mermaid diagrams (`.mmd` files) and corresponding visualizations (`.svg` or `.png`)
- **Multi-Agent**: Produces multiple outputs including sketches, repairs, and final visualizations in their respective directories

## Troubleshooting

1. **API Key Issues**: Ensure your API keys are correctly set in `src/.env`
2. **Path Errors**: Verify that all directory paths in the configuration match your local setup. Some prompts will need to be modified to match your local setup (e.g. image paths and file paths to the visuals agent).
3. **Dependency Issues**: Make sure all required packages are installed from `environment.yml`