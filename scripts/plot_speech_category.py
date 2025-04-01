import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the root of your repository
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths to the CSV files
inner_csv_path = os.path.join(repo_root, "data", "des_inner_speech.csv")
external_csv_path = os.path.join(repo_root, "data", "bnc_external_speech.csv")

# Load datasets
inner_df = pd.read_csv(inner_csv_path, na_values=[], keep_default_na=False)
external_df = pd.read_csv(external_csv_path, na_values=[], keep_default_na=False)

# --- Step 1: Normalize the speech_category values ---
def clean_category(val):
    if pd.isna(val) or val == "":
        return "N/A"
    return str(val).strip().lower().replace("  ", " ")

inner_df["in_speech_category"] = inner_df["in_speech_category"].apply(clean_category)
external_df["ext_speech_category"] = external_df["ext_speech_category"].apply(clean_category)

# --- Step 2: Count frequency of each category ---
inner_counts = inner_df["in_speech_category"].value_counts()
external_counts = external_df["ext_speech_category"].value_counts()

# --- Step 3: Combine counts into one DataFrame ---
all_categories = sorted(set(inner_counts.index).union(set(external_counts.index)))
data = {
    "Inner Speech": [inner_counts.get(cat, 0) for cat in all_categories],
    "External Speech": [external_counts.get(cat, 0) for cat in all_categories],
}
df = pd.DataFrame(data, index=all_categories)

# --- Step 4: Plot grouped bar chart ---
fig, ax = plt.subplots(figsize=(10, 6))
width = 0.35
x = range(len(df))

ax.bar([i - width/2 for i in x], df["Inner Speech"], width=width, label="Inner Speech")
ax.bar([i + width/2 for i in x], df["External Speech"], width=width, label="External Speech")

ax.set_xticks(x)
ax.set_xticklabels(df.index, rotation=45)
ax.set_xlabel("Speech Category")
ax.set_ylabel("Count")
ax.set_title("Speech Category Comparison")
ax.legend()

plt.tight_layout()

# --- Step 5: Save the figure ---
figures_dir = os.path.join(repo_root, "figures")
os.makedirs(figures_dir, exist_ok=True)
output_path = os.path.join(figures_dir, "speech_category_grouped.png")
plt.savefig(output_path)

print(f"Figure saved to: {output_path}")
