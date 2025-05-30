import pandas as pd
import krippendorff
import os

# Define the root directory of the repository
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths to annotation files for stages 2 and 3
data_paths = {
    "stage_2": {
        "annotator1": os.path.join(repo_root, "data", "annotator_1_stage_2.csv"),
        "annotator2": os.path.join(repo_root, "data", "annotator_2_stage_2.csv"),
    },
    "stage_3": {
        "annotator1": os.path.join(repo_root, "data", "annotator_1_stage_3.csv"),
        "annotator2": os.path.join(repo_root, "data", "annotator_2_stage_3.csv"),
    }
}

# Output directory
output_dir = os.path.join(repo_root, "output")
os.makedirs(output_dir, exist_ok=True)

# Process each stage
for stage, paths in data_paths.items():
    df1 = pd.read_csv(paths["annotator1"])
    df2 = pd.read_csv(paths["annotator2"])

    # Select columns from index 6 to 15 (inclusive)
    target_columns = df1.columns[6:16]

    results = []

    for column in target_columns:
        if column in df2.columns:
            values1 = df1[column].tolist()
            values2 = df2[column].tolist()
            data = [values1, values2]

            # Compute Krippendorff's alpha without skipping any columns
            alpha = krippendorff.alpha(reliability_data=data, level_of_measurement='nominal')

            results.append({
                "column": column,
                "alpha": alpha
            })

    # Save results to CSV
    result_df = pd.DataFrame(results)
    output_file = os.path.join(output_dir, f"krippendorff_alpha_{stage}.csv")
    result_df.to_csv(output_file, index=False)
