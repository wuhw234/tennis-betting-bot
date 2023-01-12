import numpy

surface_weights = {
    'm': {
        'h': 0.381,
        'c': 0.664,
        'g': 0.141
    },
    'f': {
        'h': 0.1,
        'c': 0.1,
        'g': 0.615
    }
}

def moneyline_to_probability(odds):
    if odds < 0:
        return ((-odds) / (-odds + 100))
    else:
        return (100 / (odds+100))

def elo_to_probability(player1_elo, player2_elo):
    return 1 / (1 + 10 ** ((player2_elo-player1_elo) /400))

def get_bo5_odds(bo3):
    p1 = numpy.roots([-2, 3, 0, -1*bo3])[1]
    p5 = (p1**3)*(4 - 3*p1 + (6*(1-p1)*(1-p1)))
    return p5

def get_weighted_elo(elo, yelo, matches, surface_elo, gender, surface):
    surface_weight = surface_weights[gender][surface]
    if yelo == 0 and matches == 0:
        return (1 - surface_weight) * elo + surface_weight * surface_elo
    yelo_weight = (matches / 100) * 0.5
    overall_elo = (1 - surface_weight) * elo + surface_weight * surface_elo
    return (yelo_weight * yelo) + ((1 - yelo_weight) * overall_elo) # considers both past years performance and overall performance

def get_kelly_criterion(elo_prob, moneyline_odds): #scaled kelly criterion
    if moneyline_odds > 0:
        proportion = moneyline_odds / 100
    else:
        proportion = 100 / -moneyline_odds

    return 0.25*(elo_prob - ((1-elo_prob) / proportion))

if __name__ == '__main__':
    print(get_kelly_criterion(0.8, -170))