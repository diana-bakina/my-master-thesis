import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the root of the repository
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths to the CSV files
inner_csv_path = os.path.join(repo_root, "data", "des_inner_speech.csv")
external_csv_path = os.path.join(repo_root, "data", "bnc_external_speech.csv")

# Load data
inner_df = pd.read_csv(inner_csv_path, na_values=[], keep_default_na=False)
external_df = pd.read_csv(external_csv_path, na_values=[], keep_default_na=False)

# Fill missing values for consistency
inner_df["in_speech_type"] = inner_df["in_speech_type"].fillna("missing")
inner_df["in_direction"] = inner_df["in_direction"].fillna("missing")
external_df["ext_speech_type"] = external_df["ext_speech_type"].fillna("missing")
external_df["ext_direction"] = external_df["ext_direction"].fillna("missing")

# Create cross-tabulations
inner_cross_tab = pd.crosstab(inner_df["in_speech_type"], inner_df["in_direction"])
external_cross_tab = pd.crosstab(external_df["ext_speech_type"], external_df["ext_direction"])

# Create a figure with subplots
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Inner speech plot
inner_plot = inner_cross_tab.plot(kind="bar", ax=axs[0], stacked=False)
axs[0].set_title("Inner Speech Type by Direction")
axs[0].set_xlabel("Speech Type")
axs[0].set_ylabel("Count")
axs[0].legend(title="Direction")
for container in inner_plot.containers:
    for bar in container:
        height = bar.get_height()
        if height > 0:
            axs[0].text(bar.get_x() + bar.get_width()/2, height, f"{int(height)}",
                        ha='center', va='bottom', fontsize=8)

# External speech plot
external_plot = external_cross_tab.plot(kind="bar", ax=axs[1], stacked=False,
                                        color=["#1f77b4", "#ff7f0e", "#2ca02c"])
axs[1].set_title("External Speech Type by Direction")
axs[1].set_xlabel("Speech Type")
axs[1].set_ylabel("Count")
axs[1].legend(title="Direction")
for container in external_plot.containers:
    for bar in container:
        height = bar.get_height()
        if height > 0:
            axs[1].text(bar.get_x() + bar.get_width()/2, height, f"{int(height)}",
                        ha='center', va='bottom', fontsize=8)

plt.tight_layout()

# Create a 'figures' directory if it doesn't exist
figures_dir = os.path.join(repo_root, "figures")
os.makedirs(figures_dir, exist_ok=True)

# Save the figure
output_path = os.path.join(figures_dir, "speech_type_by_direction.png")
plt.savefig(output_path)

print(f"Figure saved to: {output_path}")
