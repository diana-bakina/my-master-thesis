import os
import pandas as pd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to CSV file
csv_path = os.path.join(repo_root, "data", "inner_speech.csv")

df = pd.read_csv(csv_path)

# Calculate values in the column
counts = df["inner_speech_type"].value_counts()

print(counts)
