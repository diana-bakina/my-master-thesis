import os
import pandas as pd
from nltk.tokenize import word_tokenize
import string
import re

# Define the path to the CSV file
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(repo_root, "data", "anonymized_IS-corpus.csv")

# Load the dataset
df = pd.read_csv(data_path, encoding="utf-8-sig")

# Filter out entries where 'words' equals 'indeterminate'
filtered_df = df[df['words'].str.lower() != 'indeterminate'].copy()

# Function to clean corrupted symbols from the text
def clean_text(text):
    try:
        # Fix encoding artifacts (e.g., “вЂ™” to “'”)
        text = text.encode('latin1', errors='ignore').decode('utf-8', errors='ignore')
    except:
        pass
    # Normalize typographic quotation marks and apostrophes
    text = text.replace('’', "'").replace('“', '"').replace('”', '"')
    # Remove invisible characters and normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to count words using NLTK tokenizer
def count_words(text):
    cleaned = clean_text(text)
    tokens = word_tokenize(cleaned, preserve_line=True)
    words_only = [token for token in tokens if token not in string.punctuation]
    return len(words_only)

# Apply word counting to the filtered column
filtered_df['n_words'] = filtered_df['words'].astype(str).apply(count_words)

# Save full dataframe to CSV (with all columns + n_words)
output_csv_path = os.path.join(repo_root, "data", "IS_corpus_with_word_counts.csv")
filtered_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

# Save to Excel (for clean viewing)
output_xlsx_path = os.path.join(repo_root, "data", "IS_corpus_with_word_counts.xlsx")
filtered_df.to_excel(output_xlsx_path, index=False)
