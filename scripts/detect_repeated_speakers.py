import os

# Path to the root of the repository
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the folder containing input text files
input_folder = os.path.join(repo_root, "data", "bnc_raw")

# Get a sorted list of .txt files
text_files = sorted([f for f in os.listdir(input_folder) if f.endswith(".txt")])

# Dictionary to store first repeated speaker example per file
repeated_speaker_files = {}

# Process each file
for file_name in text_files:
    file_path = os.path.join(input_folder, file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        prev_speaker = None

        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')
            if len(parts) == 3:
                speaker, _, _ = parts
                if speaker == prev_speaker:
                    repeated_speaker_files[file_name] = line
                    break  # Stop after first repeated speaker in this file
                prev_speaker = speaker
            elif len(parts) == 2:
                # Speaker not specified, keep previous speaker unchanged
                continue
            else:
                continue  # Skip malformed lines

# Print results
for fname, example in repeated_speaker_files.items():
    print(f"{fname} — repeated speaker: {example}")
