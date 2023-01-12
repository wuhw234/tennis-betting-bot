from odds_scraper import get_odds
from elo_scraper import get_elo
from probability_calculator import moneyline_to_probability, elo_to_probability, get_bo5_odds, get_weighted_elo, get_kelly_criterion

def calculate_bet():
    gender, surface, match_type = get_user_input()
    
    match_odds = get_odds()
    elo_dict = get_elo(gender)
    positive_bets = []
    # print(match_odds)

    for hash in match_odds.keys():
        player1, player2 = hash.split('/')
        player1_moneyline, _ = max(match_odds[hash]['p1_odds'])
        player2_moneyline, _ = max(match_odds[hash]['p2_odds'])

        if player1 not in elo_dict or player2 not in elo_dict:
            continue
        player1_elo_win_prob, player2_elo_win_prob = get_elo_win_probs(player1, player2, elo_dict, gender, surface, match_type)
        sportsbook1, sportsbook2, player1_odds_win_prob, player2_odds_win_prob = get_odds_win_probs(match_odds, hash)

        max_diff = 0
        p1_diff = player1_elo_win_prob - player1_odds_win_prob
        p2_diff = player2_elo_win_prob - player2_odds_win_prob
        if p1_diff > 0 or p2_diff > 0:
            chosen_player = player1 if p1_diff > p2_diff else player2
            max_diff = max(p1_diff, p2_diff)
            if p1_diff > p2_diff:
                sportsbook = sportsbook1
            else:
                sportsbook = sportsbook2
        else:
            continue

        if chosen_player == player1:     
            kelly_value = get_kelly_criterion(player1_elo_win_prob, player1_moneyline)
        else:
            kelly_value = get_kelly_criterion(player2_elo_win_prob, player2_moneyline)

        positive_bets.append([max_diff, kelly_value, sportsbook, chosen_player, player1, player1_elo_win_prob, 
                              player1_odds_win_prob, player2, player2_elo_win_prob, player2_odds_win_prob])
    
    positive_bets.sort(reverse=True)

    output_results(positive_bets)
        
def get_user_input():
    gender = None
    while gender != 'm' and gender != 'f':
        gender = input('Is the event male or female? (m or f)')
    surface = None
    while surface != 'h' and surface != 'c' and surface != 'g':
        surface = input('Are the courts hard, clay, or grass? (h, c, or g)')
    match_type = None
    while match_type != '3' and match_type != '5':
        match_type = input('Are the matches bo3 or bo5? (3 or 5)')
    
    return gender, surface, match_type

def get_surface_string(surface):
    surface_string = None
    if surface == 'h':
        surface_string = 'hard_elo'
    elif surface == 'g':
        surface_string == 'grass_elo'
    else:
        surface_string == 'clay_elo'

    return surface_string

def get_elo_win_probs(player1, player2, elo_dict, gender, surface, match_type):
    surface_string = get_surface_string(surface)

    player1_elo, player1_surface_elo = elo_dict[player1]['elo'], elo_dict[player1][surface_string]
    player2_elo, player2_surface_elo = elo_dict[player2]['elo'], elo_dict[player2][surface_string]
    # player1_yelo, player2_yelo = elo_dict[player1]['yelo'], elo_dict[player2]['yelo'] uncomment later in the year
    # player1_matches, player2_matches = elo_dict[player1]['total_matches'], elo_dict[player2]['total_matches']
    player1_yelo, player2_yelo = 0, 0
    player1_matches, player2_matches = 0, 0
    player1_weighted_elo = get_weighted_elo(player1_elo, player1_yelo, player1_matches, player1_surface_elo, gender, surface)
    player2_weighted_elo = get_weighted_elo(player2_elo, player2_yelo, player2_matches, player2_surface_elo, gender, surface)

    player1_elo_win_prob = elo_to_probability(player1_weighted_elo, player2_weighted_elo)
    if match_type == '5':
        player1_elo_win_prob = get_bo5_odds(player1_elo_win_prob)

    player2_elo_win_prob = 1 - player1_elo_win_prob

    return player1_elo_win_prob, player2_elo_win_prob

def get_odds_win_probs(match_odds, hash):
    player1_odds, sportsbook1 = max(match_odds[hash]['p1_odds'])
    player2_odds, sportsbook2 = max(match_odds[hash]['p2_odds'])
    player1_odds_win_prob = moneyline_to_probability(player1_odds)
    player2_odds_win_prob = moneyline_to_probability(player2_odds)

    return sportsbook1, sportsbook2, player1_odds_win_prob, player2_odds_win_prob

def output_results(positive_bets):
    for max_diff, kelly_val, sportsbook, chosen_player, p1, p1_elo_win, p1_odds_win, p2, p2_elo_win, p2_odds_win in positive_bets:
        print(f'Recommended bet: {kelly_val*100}% on {chosen_player} on {sportsbook}.')
        print(f'{p1} elo win: {p1_elo_win*100}%. {p1} odds win: {p1_odds_win*100}%.')
        print(f'{p2} elo win: {p2_elo_win*100}%. {p2} odds win: {p2_odds_win*100}%.')
        print(f'Difference: {max_diff * 100}%')
        print('\n')



if __name__ == '__main__':
    calculate_bet()