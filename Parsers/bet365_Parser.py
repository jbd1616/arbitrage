import re
import csv
from bs4 import BeautifulSoup

# Load the team names from the CSV file into a dictionary
team_name_mapping = {}

with open('./Utils/team_names.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        actual_name, bet365_name = row
        team_name_mapping[bet365_name.strip()] = actual_name.strip()

# Open the HTML file with utf-8 encoding
with open('./scraper-out/output_bet365.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Find all elements with class 'pl-PodLoaderModule_Pod-61'
pod_elements = soup.find_all(class_="pl-PodLoaderModule_Pod-61")

# Iterate over each pod element to check if it contains 'NHL'
for pod in pod_elements:
    
    # Check if the class 'ss-HomeSpotlightHeader_Title ss-HomeSpotlightHeader_Title-lang32' exists inside the pod
    nhl_title = pod.find(class_="ss-HomeSpotlightHeader_Title ss-HomeSpotlightHeader_Title-lang32")
    
    if nhl_title and "NHL" in nhl_title.text:
        print("Found NHL:", nhl_title.text.strip())
        
        # Find all elements with class 'cpm-ParticipantFixtureDetailsIceHockey_Team' inside this pod
        teams = pod.find_all(class_="cpm-ParticipantFixtureDetailsIceHockey_Team")
        
        nhl_teams = []  # Initialize the array

        for team in teams:
            bet365_team_name = team.text.strip()
            actual_name = team_name_mapping.get(bet365_team_name, bet365_team_name)  # Default to bet365 name if no match
            nhl_teams.append(actual_name)  # Add the actual name to the nhl_teams array

        
        # Now, find all elements with class 'cpm-MarketOdds gl-Market_General gl-Market_General-columnheader'
        market_odds_headers = pod.find_all(class_="cpm-MarketOdds gl-Market_General gl-Market_General-columnheader")
        
        # Iterate over each market odds header
        for odds_header in market_odds_headers:
            # Check if the header string contains "money"
            if "money" in odds_header.text.lower():
                
                # Remove the word 'money' from the string
                odds_text = odds_header.text.strip().replace("money", "").strip()
                
                # Use a regex to split the string by the transition from one number to another (2 decimal places)
                odds_list = [float(x) for x in re.findall(r'\d+\.\d{2}', odds_text)]
                



# Prepare the data
games = []
for i in range(0, len(nhl_teams), 2):  # Step through the teams in pairs
    game_number = f"Game {i // 2 + 1}"  # Generate the game number
    team_1 = nhl_teams[i]
    moneyline_1 = odds_list[i]
    team_2 = nhl_teams[i + 1]
    moneyline_2 = odds_list[i + 1]
    games.append([game_number, team_1, moneyline_1, team_2, moneyline_2])

# Write to CSV
with open('./parser-out/bet365_results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header
    writer.writerow(['Game', 'Team 1', 'moneyline 1', 'Team 2', 'moneyline 2'])

    # Write the rows
    writer.writerows(games)

print("Data has been written to bet365_results.csv in the specified format.")