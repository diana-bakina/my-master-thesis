import os
import pandas as pd
import matplotlib.pyplot as plt

# Define repository root
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths to data files
inner_csv_path = os.path.join(repo_root, "data", "des_inner_speech.csv")
external_csv_path = os.path.join(repo_root, "data", "bnc_external_speech.csv")

# Load data
inner_df = pd.read_csv(inner_csv_path, na_values=[], keep_default_na=False)
external_df = pd.read_csv(external_csv_path, na_values=[], keep_default_na=False)

# Clean text: strip whitespace and convert to lowercase
inner_df["in_speech_function"] = inner_df["in_speech_function"].str.strip().str.lower()
external_df["ext_speech_function"] = external_df["ext_speech_function"].str.strip().str.lower()

# Count speech functions
inner_counts = inner_df["in_speech_function"].fillna("missing").value_counts()
external_counts = external_df["ext_speech_function"].fillna("missing").value_counts()

# Combine into a single DataFrame
function_df = pd.DataFrame({
    "Inner Speech": inner_counts,
    "External Speech": external_counts
}).fillna(0).astype(int).sort_values(by="Inner Speech", ascending=False)

# Create 'figures' directory if it doesn't exist
figures_dir = os.path.join(repo_root, "figures")
os.makedirs(figures_dir, exist_ok=True)

# Plot bar chart
ax = function_df.plot(kind="bar", figsize=(14, 6))
plt.title("Speech Function Frequency Comparison")
plt.xlabel("Speech Function")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.legend(title="Corpus")
plt.tight_layout()

# Save the bar chart
output_path = os.path.join(figures_dir, "speech_function_comparison.png")
plt.savefig(output_path)
print(f"Figure saved to: {output_path}")

# Create and save a table image
fig, ax = plt.subplots(figsize=(8, 0.5 + 0.4 * len(function_df)))  # adjust height dynamically
ax.axis('tight')
ax.axis('off')

# Create table
table = ax.table(
    cellText=function_df.values,
    colLabels=function_df.columns,
    rowLabels=function_df.index,
    loc='center',
    cellLoc='center'
)

table.scale(1, 1.5)
table.auto_set_font_size(False)
table.set_fontsize(10)

# Save the table image
table_path = os.path.join(figures_dir, "speech_function_table.png")
plt.savefig(table_path, bbox_inches='tight')
print(f"Table image saved to: {table_path}")
