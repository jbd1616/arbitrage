#odds_translator.py

def AtoD(odds):

    length = len(odds)

    # underdog odds
    if odds[0] == '+':
        odds = int(odds[1:])
        decimal_odds = (odds/100) + 1

    elif odds[0] == '-':
        odds = int(odds[1:])
        decimal_odds = (100/odds) + 1

    else:
        print("Error in odds convertor")
        decimal_odds = "error"

    return decimal_odds
