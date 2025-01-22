moneyline3 = 1.7
moneyline4 = 2.65

total_probability2 = (1/moneyline3) + (1/moneyline4)

print(total_probability2)

if total_probability2 < 1:
    total_bet = 10
    money_to_bet1 = total_bet / moneyline3
    money_to_bet2 = total_bet / moneyline4
    normalization_factor = 10 / (money_to_bet1 + money_to_bet2)

    money_to_bet1 = round(normalization_factor*money_to_bet1, 2)
    money_to_bet2 = round(normalization_factor*money_to_bet2, 2)

    winnings1 = money_to_bet1*moneyline3
    winnings2 = money_to_bet2*moneyline4

    print("odds:", moneyline3)
    print("money to place:", money_to_bet1)
    print(winnings1)
    print("ROI:", winnings1/10)

    print("odds:", moneyline4)
    print("money to place:", money_to_bet2)
    print(winnings2)
    print("ROI:", winnings2/10)
else:
    print("not a good bet")
