import os
import pandas as pd
import random

# Define the root of the repository
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the parsed conversation CSV
input_path = os.path.join(repo_root, "data", "bnc_parsed.csv")

# Load the parsed conversation table
df = pd.read_csv(input_path)

# Store the results
beep_rows = []

# Group by conversation file
for file, group in df.groupby("file"):
    # Sort rows by original order in the file
    group = group.sort_values("line_id").reset_index(drop=True)

    full_text = ""
    char_map = []  # List of (row_index, word_index, char_index)

    for idx, row in group.iterrows():
        raw_text = row["text"]

        # Treat missing or annotator-written "None" as empty text
        if pd.isna(raw_text) or str(raw_text).strip().lower() == "none":
            text = ""
        else:
            text = str(raw_text)

        words = text.split()
        for w_i, word in enumerate(words):
            for c_i in range(len(word)):
                char_map.append((idx, w_i, c_i))
        full_text += text + " "

    if len(char_map) < 2:
        continue  # Skip very short conversations

    # Choose 2 random character positions to insert [BEEP]
    beep_positions = random.sample(range(len(char_map)), 2)

    # Create an empty column for beep-modified text
    group["text_with_beep"] = None

    for pos in beep_positions:
        row_idx, word_idx, char_idx = char_map[pos]
        raw_text = group.loc[row_idx, "text"]

        # Same safe check for beep injection
        if pd.isna(raw_text) or str(raw_text).strip().lower() == "none":
            continue

        text = str(raw_text)
        words = text.split()

        if word_idx >= len(words):
            continue

        word = words[word_idx]
        if char_idx >= len(word):
            continue

        # Insert [BEEP] into the word
        new_word = word[:char_idx] + "[BEEP]" + word[char_idx:]
        words[word_idx] = new_word
        new_text = " ".join(words)

        group.at[row_idx, "text_with_beep"] = new_text

    beep_rows.append(group)

# Combine all modified groups
df_with_beeps = pd.concat(beep_rows).reset_index(drop=True)

# Save the result to CSV
output_path = os.path.join(repo_root, "data", "bnc_with_beeps.csv")
df_with_beeps.to_csv(output_path, index=False)
