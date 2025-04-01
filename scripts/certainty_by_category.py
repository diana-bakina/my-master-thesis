import os
import pandas as pd
import matplotlib.pyplot as plt

# Define repo root
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths
inner_path = os.path.join(repo_root, "data", "des_inner_speech.csv")
external_path = os.path.join(repo_root, "data", "bnc_external_speech.csv")

# Load data
inner_df = pd.read_csv(inner_path, na_values=[], keep_default_na=False)
external_df = pd.read_csv(external_path, na_values=[], keep_default_na=False)

# Clean values
def clean(val):
    if pd.isna(val) or val == "":
        return "N/A"
    return str(val).strip().lower().replace("  ", " ")

external_df["ext_speech_category"] = external_df["ext_speech_category"].apply(clean)
external_df["ext_reconstruction_certainty"] = external_df["ext_reconstruction_certainty"].apply(clean)

inner_df["in_speech_category"] = inner_df["in_speech_category"].apply(clean)
inner_df["in_speech_certainty"] = inner_df["in_speech_certainty"].apply(clean)

# Helper to build and save table as image
def save_table_image(df, index_col, certainty_col, output_path, title):
    counts = pd.crosstab(df[index_col], df[certainty_col])
    counts["total"] = counts.sum(axis=1)
    counts["% certain"] = (counts.get("certain", 0) / counts["total"] * 100).round(1)
    counts = counts.sort_values(by="% certain", ascending=False)

    fig, ax = plt.subplots(figsize=(8, 0.5 + 0.5 * len(counts)))
    ax.axis('off')
    ax.axis('tight')

    table = ax.table(
        cellText=counts.values,
        colLabels=counts.columns,
        rowLabels=counts.index,
        cellLoc='center',
        loc='center'
    )
    table.scale(1, 1.4)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    plt.title(title, pad=20)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    print(f"Saved table to: {output_path}")

# Save both tables
figures_dir = os.path.join(repo_root, "figures")
os.makedirs(figures_dir, exist_ok=True)

ext_table_path = os.path.join(figures_dir, "external_certainty_table.png")
inner_table_path = os.path.join(figures_dir, "inner_certainty_table.png")

save_table_image(
    external_df,
    index_col="ext_speech_category",
    certainty_col="ext_reconstruction_certainty",
    output_path=ext_table_path,
    title="External Speech: Certainty by Speech Category"
)

save_table_image(
    inner_df,
    index_col="in_speech_category",
    certainty_col="in_speech_certainty",
    output_path=inner_table_path,
    title="Inner Speech: Certainty by Speech Category"
)
