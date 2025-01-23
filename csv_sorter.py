import pandas as pd

# Load the CSV files into DataFrames
file1_df = pd.read_csv("bet365_results.csv")  # Replace with the path to your first CSV file (e.g., B365)
file2_df = pd.read_csv("fanduel_results.csv")  # Replace with the path to your second CSV file (e.g., FD)

# Strip any leading or trailing spaces from column names (common issue with CSV files)
file1_df.columns = file1_df.columns.str.strip()
file2_df.columns = file2_df.columns.str.strip()

# Create a dictionary mapping the team pairs to their game number from file1_df
game_mapping = {}

for _, row in file1_df.iterrows():
    # Create a tuple with the teams for the game
    team_pair = tuple(sorted([row['Team 1'], row['Team 2']]))
    game_mapping[team_pair] = row['Game']

# Iterate through file2_df and update the Game column based on team pairs
for _, row in file2_df.iterrows():
    team_pair = tuple(sorted([row['Team 1'], row['Team 2']]))
    if team_pair in game_mapping:
        file2_df.at[_, 'Game'] = game_mapping[team_pair]

# Save the updated DataFrame to a new CSV file
file2_df.to_csv("fanduel_results.csv", index=False)

# Optional: Print the updated DataFrame for verification
print(file2_df.head())
