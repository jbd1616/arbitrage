import pandas as pd

# Load the CSV files into DataFrames
file1_df = pd.read_csv("./parser-out/bet365_results.csv")  # Replace with the path to your first CSV file (e.g., B365)
file2_df = pd.read_csv("./parser-out/fanduel_results.csv")  # Replace with the path to your second CSV file (e.g., FD)

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
file2_df.to_csv("./parser-out/fanduel_results.csv", index=False)

##NOW WITH NEW FILES WE WILL COMBINE THE DATA

# Load the CSV files into DataFrames
file1_df = pd.read_csv("./parser-out/bet365_results.csv")  # Replace with the path to your first CSV file (e.g., B365)
file2_df = pd.read_csv("./parser-out/fanduel_results.csv")  # Replace with the path to your second CSV file (e.g., FD)

# Strip any leading or trailing spaces from column names (common issue with CSV files)
file1_df.columns = file1_df.columns.str.strip()
file2_df.columns = file2_df.columns.str.strip()

# Add a column to each dataframe to indicate the source file
file1_df['Source'] = 'B365'
file2_df['Source'] = 'FD'

# Combine the two DataFrames into one
combined_df = pd.concat([file1_df, file2_df], ignore_index=True)

# Initialize an empty list to store the best odds for each team
best_odds_list = []

# Iterate over each game and team
for game in combined_df['Game'].unique():  # Loop through each unique game
    game_df = combined_df[combined_df['Game'] == game]
    
    # Iterate through both teams in each game
    for team_column in ['Team 1', 'Team 2']:
        if team_column in game_df.columns:
            for team in game_df[team_column].unique():  # Loop through each unique team in the current game
                team_df = game_df[game_df[team_column] == team]
                
                # Find the row with the best odds for the team
                best_row = team_df.loc[team_df['moneyline 1'].idxmax() if team_column == 'Team 1' else team_df['moneyline 2'].idxmax()]
                
                # Append the result to the list
                best_odds_list.append([game, team, best_row['moneyline 1'] if team_column == 'Team 1' else best_row['moneyline 2'], best_row['Source']])

# Convert the best odds list to a DataFrame for better readability
best_odds_df = pd.DataFrame(best_odds_list, columns=["Game", "Team", "Best Odds", "Source File"])

# Drop duplicate entries for the same team, keeping only the best odds
best_odds_df = best_odds_df.loc[best_odds_df.groupby(['Game', 'Team'])['Best Odds'].idxmax()]

# Reformat the output grouped by game
grouped_output = best_odds_df.groupby("Game").apply(
    lambda x: x[['Team', 'Best Odds', 'Source File']].to_dict(orient='records')
).reset_index(name='Details')

# Save the reformatted output to a JSON file for better readability
grouped_output.to_json("best_odds_by_game.json", orient='records', indent=4)

# Print the reformatted output for verification
print(grouped_output)
