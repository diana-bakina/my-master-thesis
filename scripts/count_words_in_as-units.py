import os
import pandas as pd
from nltk.tokenize import word_tokenize
import string
import re

# Define the path to the CSV file
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(repo_root, "data", "anonymized_ES-corpus.csv")

# Load the dataset
df = pd.read_csv(data_path, encoding="utf-8-sig")

# Filter out entries where 'words' equals 'indeterminate'
filtered_df = df[df['words'].str.lower() != 'indeterminate'].copy()

# Function to clean corrupted symbols from the text
def clean_text(text):
    try:
        text = text.encode('latin1', errors='ignore').decode('utf-8', errors='ignore')
    except:
        pass
    text = text.replace('’', "'").replace('“', '"').replace('”', '"')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to count words excluding <pause>, <unclear>, [BEEP], and cleaning embedded [BEEP]
def count_words(text):
    text = clean_text(text)
    text = re.sub(r'<(pause|unclear)>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\[(BEEP|pause)]', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    # Match words, including contractions like don't, they're, etc.
    words = re.findall(r"\b[\w']+\b", text)
    return len(words)


# Apply word counting
filtered_df['n_words'] = filtered_df['words'].astype(str).apply(count_words)

# Save to CSV and Excel
output_csv_path = os.path.join(repo_root, "data", "ES_corpus_with_word_counts.csv")
filtered_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

output_xlsx_path = os.path.join(repo_root, "data", "ES_corpus_with_word_counts.xlsx")
filtered_df.to_excel(output_xlsx_path, index=False)
