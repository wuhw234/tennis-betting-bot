def moneyline_to_probability(odds):
    if odds < 0:
        return (odds / (odds+100)) * 100
    else:
        return (100 / (odds+100)) * 100

def elo_to_probability(player1_elo, player2_elo):
    pass
