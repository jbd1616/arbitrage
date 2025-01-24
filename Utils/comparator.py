import json

# Read the JSON file
with open("best_odds_by_game.json", "r") as file:
    grouped_output = json.load(file)

# Loop through each game
for game_entry in grouped_output:
    game = game_entry["Game"]
    details = game_entry["Details"]
    print(f"\nGame: {game}")

    # Extract moneyline odds and their sources for this game
    if len(details) >= 2:
        moneyline1 = details[0]["Best Odds"]
        moneyline2 = details[1]["Best Odds"]
        source1 = details[0]["Source File"]
        source2 = details[1]["Source File"]
        team1 = details[0]["Team"]
        team2 = details[1]["Team"]

        # Calculate the total probability
        total_probability = (1 / moneyline1) + (1 / moneyline2)

        if total_probability < 1:  # Check if it's a good bet
            total_bet = 10  # Total stake
            money_to_bet1 = total_bet / moneyline1
            money_to_bet2 = total_bet / moneyline2
            normalization_factor = total_bet / (money_to_bet1 + money_to_bet2)

            # Normalize and round bets
            money_to_bet1 = round(normalization_factor * money_to_bet1, 2)
            money_to_bet2 = round(normalization_factor * money_to_bet2, 2)

            # Calculate winnings
            winnings1 = round(money_to_bet1 * moneyline1, 2)
            winnings2 = round(money_to_bet2 * moneyline2, 2)

            # Print results
            print("Good Bet Found!")
            print(f"  - Team: {team1}, Odds: {moneyline1}, Book: {source1}")
            print(f"    Money to place: {money_to_bet1}, Winnings: {winnings1}, ROI: {round(winnings1 / total_bet, 2)}")

            print(f"  - Team: {team2}, Odds: {moneyline2}, Book: {source2}")
            print(f"    Money to place: {money_to_bet2}, Winnings: {winnings2}, ROI: {round(winnings2 / total_bet, 2)}")
        else:
            print("No good bets found for this game.")
    else:
        print("Insufficient data for this game.")

