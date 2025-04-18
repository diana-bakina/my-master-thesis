import os
import re

# Path to the project root
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the input large file
input_path = os.path.join(repo_root, "data", "full_transcript.txt")

# Folder to save individual conversations
output_dir = os.path.join(repo_root, "data", "bnc_raw")
os.makedirs(output_dir, exist_ok=True)

# Read the entire text
with open(input_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove the final "End" block if present
content = re.sub(r'\n-+\s*End\s*-+\s*\Z', '', content)

# Split by the full line with "New Conversation <number>"
conversations = re.split(r'\n-+\s*New Conversation (\d+)\s*-+\n', content)

# Process and save conversations without repeated speaker names
for i in range(1, len(conversations), 2):
    conv_id = conversations[i]
    conv_text = conversations[i + 1].strip()

    lines = conv_text.splitlines()
    prev_speaker = None
    has_repeated_speakers = False

    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) == 3:
            speaker, _, _ = parts
            if speaker == prev_speaker:
                print(f"conversation_{conv_id}.txt — repeated speaker: {line}")
                has_repeated_speakers = True
                break
            prev_speaker = speaker
        elif len(parts) == 2:
            continue  # line without speaker, skip
        else:
            continue  # malformed line, skip

    if not has_repeated_speakers:
        filename = f"conversation_{conv_id}.txt"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(conv_text)
