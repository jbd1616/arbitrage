import pandas as pd
from bs4 import BeautifulSoup

# Load the CSV translator into a DataFrame
translator_df = pd.read_csv("team_names.csv")  # Replace with your CSV file path

# Clean up the column names and handle any extra spaces
translator_df.columns = translator_df.columns.str.strip()

# Handle any missing or incomplete data by dropping rows with empty 'bet365_names' or 'actual_names'
translator_df = translator_df.dropna(subset=['bet365_names', 'actual_names'])

# Convert the bet365_names to lowercase and strip extra spaces for better matching
translator_df['bet365_names'] = translator_df['bet365_names'].str.strip().str.lower()
translator_df['actual_names'] = translator_df['actual_names'].str.strip()

# Create a dictionary mapping from bet365_names (lowercase) to actual_names
name_mapping = dict(zip(translator_df["bet365_names"], translator_df["actual_names"]))

# Open the HTML file
with open("output_bet365.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Initialize lists to store the results
game_results = []

# Find the NHL section header
nhl_section = soup.find("div", class_="ss-HomeSpotlightHeader_Title ss-HomeSpotlightHeader_Title-lang32")
if nhl_section and "NHL" in nhl_section.text:
    print("NHL section found. Parsing the teams and odds...")

    # Find all the team containers first
    team_elements = soup.find_all("div", class_="cpm-ParticipantFixtureDetailsIceHockey_Team")
    
    # Store all the teams in the correct order
    teams = []
    for team in team_elements:
        team_name = team.text.strip().lower()
        if team_name in name_mapping:
            translated_name = name_mapping[team_name]
            teams.append(translated_name)

    # Find the "cpm-MarketOdds" section and check if it contains the Money header
    market_odds_section = soup.find_all("div", class_="cpm-MarketOdds gl-Market_General gl-Market_General-columnheader")
    
    for section in market_odds_section:
        # Check if the immediate child has the "Money" header
        money_header = section.find("div", class_="cpm-MarketOddsHeader")
        if money_header and "Money" in money_header.text:
            print("Found Money header. Extracting moneyline odds...")

            # Now, find all the odds elements that match the specified classes
            odds_elements_1 = section.find_all("span", class_="cpm-ParticipantOdds_Odds")
            
            # If odds are found, make sure they match the number of teams
            if len(odds_elements_1) == len(teams):
                moneyline_odds = [odd.text.strip() for odd in odds_elements_1]

                # Pair teams and their corresponding odds sequentially
                for idx in range(0, len(teams), 2):
                    team1 = teams[idx]
                    team2 = teams[idx + 1] if idx + 1 < len(teams) else None
                    moneyline1 = moneyline_odds[idx] if idx < len(moneyline_odds) else ""
                    moneyline2 = moneyline_odds[idx + 1] if (idx + 1) < len(moneyline_odds) else ""

                    # Append the game result
                    game_results.append([f"Game {idx // 2 + 1}", team1, moneyline1, team2, moneyline2])
            else:
                print(f"Warning: Number of odds ({len(odds_elements_1)}) does not match the number of teams ({len(teams)}).")
                # Proceed to write the team names only
                for idx in range(0, len(teams), 2):
                    team1 = teams[idx]
                    team2 = teams[idx + 1] if idx + 1 < len(teams) else None
                    game_results.append([f"Game {idx // 2 + 1}", team1, "", team2, ""])
            
            break  # We only need to process the first valid market section
    
else:
    print("NHL section not found in the HTML. Parsing skipped.")

# Convert the results into a DataFrame
game_results_df = pd.DataFrame(game_results, columns=["Game", "Team 1", "moneyline 1", "Team 2", "moneyline 2"])

# Output the results to a CSV file
game_results_df.to_csv("bet365_results.csv", index=False)

# Print the output for verification
print("Translated game results saved to bet365_results.csv.")
