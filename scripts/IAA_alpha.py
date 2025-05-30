import pandas as pd
import krippendorff
import os

# Path to the root of the repository
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths to annotator files for stage 3
annotator1_path = os.path.join(repo_root, "data", "annotator_1_stage_3.csv")
annotator2_path = os.path.join(repo_root, "data", "annotator_2_stage_3.csv")

# Load data
annotator1_df = pd.read_csv(annotator1_path)
annotator2_df = pd.read_csv(annotator2_path)

# Column range: index 6 to 15 (inclusive)
target_columns = annotator1_df.columns[6:16]

for i, col in enumerate(annotator1_df.columns):
    print(f"{i}: {col}")

print("\nCalculating Krippendorff's alpha:\n")

for column in target_columns:
    column = column.strip()

    if column not in annotator2_df.columns:
        print(f"Skipped (missing in annotator2): {column}")
        continue

    try:
        values1 = annotator1_df[column].tolist()
        values2 = annotator2_df[column].tolist()
        data = [values1, values2]

        alpha = krippendorff.alpha(reliability_data=data, level_of_measurement='nominal')
        print(f"{column}: Krippendorff's alpha = {alpha}")
    except Exception as e:
        print(f"Error in column '{column}': {e}")
