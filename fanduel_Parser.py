
import re
import pandas as pd
from odds_translator import AtoD

# List of national teams to exclude
national_teams = [
    "Canada", "USA", "Russia", "Finland", "Sweden", "Czech Republic",
    "Slovakia", "Germany", "Switzerland", "Latvia", "Denmark", "Norway", "Belarus"
]

# Read the HTML file
with open('output_fanduel.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Extract Moneyline odds using regular expression
moneyline_pattern = re.compile(r'label="Moneyline, ([^,]+), ([^,]+) Odds"')
moneyline_matches = moneyline_pattern.findall(html_content)

# Initialize arrays for Team1, Team2, Odds1, and Odds2
Team1 = []
Team2 = []
Odds1 = []
Odds2 = []

# Alternate between placing teams and odds into the arrays
for i, match in enumerate(moneyline_matches):
    team_name = match[0].strip()
    odds = AtoD(match[1].strip())

    # Check if the team is not in the national_teams list
    if team_name not in national_teams:
        if i % 2 == 0:  # Even index (1st, 3rd, 5th, etc.) goes to Team1 and Odds1
            Team1.append(team_name)
            Odds1.append(odds)
        else:  # Odd index (2nd, 4th, 6th, etc.) goes to Team2 and Odds2
            Team2.append(team_name)
            Odds2.append(odds)

# Load the CSV file into a DataFrame
df = pd.read_csv('bet365_results.csv')

# Get the length of a specific column
column_length = len(df['Game'])

# Compare lengths and adjust Team1, Team2, Odds1, and Odds2 arrays if necessary
if len(Team1) > column_length:
    # If Team1 is longer than column_length, trim the arrays
    Team1 = Team1[:column_length]
    Team2 = Team2[:column_length]
    Odds1 = Odds1[:column_length]
    Odds2 = Odds2[:column_length]

# Create a DataFrame with the required columns
games = [f"Game {i+1}" for i in range(len(Team1))]  # Generate game labels like Game1, Game2, etc.
data = {
    "Game": games,
    "Team 1": Team1,
    "moneyline 1": Odds1,
    "Team 2": Team2,
    "moneyline 2": Odds2
}

# Create the DataFrame and save to CSV
results_df = pd.DataFrame(data)
results_df.to_csv("fanduel_results.csv", index=False)

print("Results printed to fanduel_results.csv")