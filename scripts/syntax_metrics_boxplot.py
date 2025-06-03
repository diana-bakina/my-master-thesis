import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Paths to data
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
is_path = os.path.join(repo_root, "data", "IS_corpus_with_metrics.csv")
es_path = os.path.join(repo_root, "data", "ES_corpus_with_metrics.csv")

# Load data
is_df = pd.read_csv(is_path)
es_df = pd.read_csv(es_path)

# Rename columns for consistency
is_df = is_df.rename(columns={
    "W_per_IE": "W_per_Unit",
    "C_per_IE": "C_per_Unit",
    "Coord_per_IE": "Coord_per_Unit"
})

es_df = es_df.rename(columns={
    "W_per_AS": "W_per_Unit",
    "C_per_AS": "C_per_Unit",
    "Coord_per_AS": "Coord_per_Unit"
})

# --- Merge datasets ---
is_df["group"] = "Inner Speech"
es_df["group"] = "External Speech"
df = pd.concat([is_df, es_df], ignore_index=True)

# --- Metrics and labels ---
metrics = ["W_per_Unit", "C_per_Unit", "Coord_per_Unit", "DC_per_C", "W_per_C"]
titles = {
    "W_per_Unit": "Words per Unit (W/Unit)",
    "C_per_Unit": "Clauses per Unit (C/Unit)",
    "Coord_per_Unit": "Coordinated Clauses per Unit (Coord/Unit)",
    "DC_per_C": "Dependent Clauses per Clause (DC/C)",
    "W_per_C": "Words per Clause (W/C)"
}

# --- Plot combined figure with subplots ---
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(14, 12))
axes = axes.flatten()

for i, metric in enumerate(metrics):
    sns.boxplot(data=df, x="group", y=metric, ax=axes[i])
    axes[i].set_title(titles[metric])
    axes[i].set_xlabel("Speech Type")
    axes[i].set_ylabel(titles[metric])

# Remove empty subplot if fewer metrics than axes
if len(metrics) < len(axes):
    fig.delaxes(axes[-1])

# --- Save figure ---
plt.tight_layout()
output_path = os.path.join(repo_root, "figures", "syntax_complexity_boxplots.png")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Plot saved to: {output_path}")
