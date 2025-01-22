import re
import csv
from odds_translator import AtoD

# List of national teams to exclude (you can add more if needed)
national_teams = ["Canada", "USA", "Russia", "Finland", "Sweden", "Czech Republic", "Slovakia", "Germany", "Switzerland", "Latvia", "Denmark", "Norway", "Belarus"]

# Define a custom class to represent each game
class Game:
    def __init__(self, team_1, odds_1, team_2, odds_2):
        self.team_1 = team_1
        self.odds_1 = moneyline_1
        self.team_2 = team_2
        self.odds_2 = moneyline_2

    def to_list(self):
        # Convert the Game object to a list that can be written to a CSV
        return [self.team_1, self.moneyline_1, self.team_2, self.moneyline_2]

# Open the HTML file in read mode
with open("output_fanduel.html", "r", encoding="utf-8") as file:
    # Read the entire file content
    html_content = file.read()

# Normalize the HTML content by removing extra whitespace and newlines
normalized_content = " ".join(html_content.split())

# Define the normalized snippet to search for team names
search_snippet = '"@type": "SportsEvent", "name":'

# Use regular expression to find all occurrences of the team names (including ' @ ')
pattern = re.compile(r'"@type": "SportsEvent", "name":\s*"([^"]+)"')
matches = pattern.findall(normalized_content)

# Split the teams based on '@' and filter out national teams
filtered_teams = []
for match in matches:
    teams = match.split(" @ ")
    if len(teams) == 2:  # Make sure there are two teams in the match
        team_1, team_2 = teams
        # Check if both teams are not national teams
        if not any(national_team in team_1 for national_team in national_teams) and \
           not any(national_team in team_2 for national_team in national_teams):
            filtered_teams.append([team_1, team_2])  # Add the teams as a row

# Define the pattern to search for Moneyline odds for each team
moneyline_pattern = re.compile(r"Moneyline, ([^,]+), ([^,]+) Odds")

# Use regular expression to find all Moneyline occurrences and their odds
moneyline_matches = moneyline_pattern.findall(normalized_content)

# Create a dictionary to store the odds for each team
team_odds = {}
for match in moneyline_matches:
    team_name = match[0]
    odds = match[1]
    team_odds[team_name] = odds  # Store the odds by team name


# Now, let's match the teams with their odds in the filtered_teams array and create Game objects
games = []
for team_1, team_2 in filtered_teams:
    moneyline_1 = AtoD(team_odds.get(team_1, "N/A"))  # Get odds for team 1, default to "N/A" if not found
    moneyline_2 = AtoD(team_odds.get(team_2, "N/A"))  # Get odds for team 2, default to "N/A" if not found
    game = Game(team_1, moneyline_1, team_2, moneyline_2)  # Create a Game object
    games.append(game)


# Write the data to a CSV file
with open("fanduel_results.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Game", "Team 1", "moneyline 1", "Team 2", "moneyline 2"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()  # Write the header row
    
    for game_num, game in enumerate(games, start=1):
        if game_num <= 8:  # Only write the first 8 games
            writer.writerow({
                "Game": f"Game {game_num}",
                "Team 1": game.team_1,
                "moneyline 1": game.odds_1,
                "Team 2": game.team_2,
                "moneyline 2": game.odds_2
            })

print("Data has been written to 'fanduel_results.csv'")
