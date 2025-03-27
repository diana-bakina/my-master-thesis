import os
import pandas as pd

# Path to the root of the repository
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the folder containing input text files
input_folder = os.path.join(repo_root, "data", "bnc_raw")

# Get a sorted list of .txt files (by name)
text_files = sorted([f for f in os.listdir(input_folder) if f.endswith(".txt")])

# List to store all parsed rows
rows = []
global_line_id = 0  # Keeps global line order across all files

# Process each text file
for file_name in text_files:
    file_path = os.path.join(input_folder, file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        current_speaker = None  # Last known speaker

        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            parts = line.split('\t')
            if len(parts) == 3:
                speaker, turn, text = parts
                current_speaker = speaker
            elif len(parts) == 2:
                turn, text = parts
                speaker = current_speaker
            elif len(parts) == 3 and parts[1].strip() == "":
                # Case: speaker \t \t text (empty turn)
                speaker, _, text = parts
                turn = None
                current_speaker = speaker
            else:
                continue  # skip malformed lines
            rows.append({
                "file": file_name,
                "line_id": global_line_id,  # Preserve original order
                "speaker": speaker,
                "turn": turn.strip() if turn.strip() else None,
                "text": text.strip()
            })
            global_line_id += 1

# Create DataFrame and save to CSV
df = pd.DataFrame(rows)
output_path = os.path.join(repo_root, "data", "bnc_parsed.csv")
df.to_csv(output_path, index=False)
