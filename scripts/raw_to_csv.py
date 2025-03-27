import os
import pandas as pd

# Path to the root of the repository
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the folder with input files
folder_path = os.path.join(repo_root, "data", "bnc_raw")

# Get list of .txt files
files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

# Storage for all rows
data = []

# Process each file
for filename in files:
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "r", encoding="utf-8") as file:
        current_speaker = None  # remember the last speaker

        for line in file:
            line = line.strip()
            if not line:
                continue  # skip empty lines

            parts = line.split('\t')
            if len(parts) == 3:
                # Format: speaker \t turn \t text
                speaker, turn, text = parts
                current_speaker = speaker
            elif len(parts) == 2:
                # Format: turn \t text (speaker is same as previous)
                turn, text = parts
                speaker = current_speaker
            else:
                continue  # skip malformed lines

            data.append({
                "file": filename,
                "speaker": speaker,
                "turn": int(turn),
                "text": text.strip()
            })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv(os.path.join(repo_root, "data", "bnc_parsed.csv"), index=False)
