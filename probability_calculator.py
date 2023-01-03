def moneyline_to_probability(odds):
    if odds < 0:
        return (odds / (odds+100)) * 100
    else:
        return (100 / (odds+100)) * 100

def elo_to_probability(player1_elo, player2_elo):
    return 1 / (1 + 10 ** ((player2_elo-player1_elo) /400))

def convert_bo3_to_bo5(bo3_prob):
    pass

if __name__ == "__main__":
    player1 = int(input('player 1 rating'))
    player2 = int(input('player 2 rating'))
    print(elo_to_probability(player1, player2))
