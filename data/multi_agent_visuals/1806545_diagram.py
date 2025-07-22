## Markdown Cell
# Diagram of Workflow

## Code Cell
# Import libraries for diagram creation
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Define variables and their flow
data_sources = ["train.csv", "test.csv"]
data_variables = ["train", "test", "y_train", "all_data", "stacked_pred"]
models = ["Kernel Ridge", "Lasso", "ElasticNet", "Gradient Boosting", "XGBoost", "LightGBM", "Stacking Averaged Models"]

# Add each data source
for i, source in enumerate(data_sources):
    ax.text(0, 5-i, f"Load {source}", fontsize=12)

# Draw flow lines and add variable nodes
for i, var in enumerate(data_variables):
    ax.text(2, 5-i, var, fontsize=12, ha='left')
    if i > 0:
        plt.plot([0.2, 2], [5-i+0.2, 4.5-i+0.2], color="black", lw=1)
    
# Add model nodes
for i, model in enumerate(models):
    ax.text(4, 5-i, model, fontsize=12, ha='left')

# Draw flow to model nodes
for i in range(len(data_variables)):
    plt.plot([2.2, 4], [5-i+0.2, 5-i+0.2], color="black", lw=1)

# Add a title and description
plt.title('Workflow Diagram for Data Science Project', fontsize=14)
plt.axis('off')

# Save the diagram
plt.savefig('distil1000/multi_agent_visuals/1806545_diagram.png')
plt.show()