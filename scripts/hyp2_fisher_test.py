from scipy.stats import fisher_exact

# Data:
# External speech: 18 ellipses, 55 without ellipsis
# Internal speech: 7 ellipses, 66 without ellipsis

# Build the 2×2 contingency table
table = [[18, 55],
         [7, 66]]

# Run Fisher's exact test (two-sided)
oddsratio, p_value = fisher_exact(table, alternative='two-sided')

print(f"Odds ratio: {oddsratio:.2f}")
print(f"P-value (Fisher's exact test): {p_value:.3f}")
