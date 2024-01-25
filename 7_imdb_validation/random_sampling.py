import pandas as pd
import random

# Load the CSV file into a DataFrame
df = pd.read_csv('metadata_for_validation.csv', dtype={"movie_id": str})

# Create a dictionary to store DataFrames for each 'dir' category
dir_dfs = {}

## REMOVE the rows 

# Iterate over unique 'dir' categories
for directory in df['dir'].unique():
    # Select rows for the current 'dir' category
    dir_rows = df[df['dir'] == directory]
    
    # Randomly sample 30 rows
    sampled_rows = dir_rows.sample(n=min(30, len(dir_rows)), random_state=42)
    
    # Store the sampled DataFrame in the dictionary
    dir_dfs[directory] = sampled_rows

# Save each DataFrame to a separate CSV file
for directory, sampled_df in dir_dfs.items():
    file_name = f'{directory}_sampled.csv'
    sampled_df.to_csv(file_name, index=False)

print("Sampling and saving completed.")
