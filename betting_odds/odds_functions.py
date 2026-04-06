def american_to_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return abs(odds) / (100 - odds)

def american_to_probability_average(odds, opp_odds):
    odds_pct = american_to_probability(odds)
    opp_odds_pct = american_to_probability(opp_odds)
    return (odds_pct) / (odds_pct + opp_odds_pct)

def american_to_probability_average_multi(odds, opp_odds_list):
    odds_pct = american_to_probability(odds)
    opp_odds_pct = sum([american_to_probability(opp_odds) for opp_odds in opp_odds_list])
    return (odds_pct) / (odds_pct + opp_odds_pct)

def profit_from_win(odds, bet=100):
    if odds > 0:
        return (odds / 100) * bet
    else:
        return 100 * (bet / abs(odds))

def even_split_bet_amounts(odds_1, odds_2, total_bet=1):
    probability = american_to_probability_average(odds_1, odds_2)
    bet_1 = probability * total_bet
    bet_2 = (1 - probability) * total_bet
    return bet_1, bet_2

def even_split_bet_amounts_multi(odds, opp_odds_list, total_bet=1):
    probability = american_to_probability_average_multi(odds, opp_odds_list)
    bet_1 = probability * total_bet
    other_bets = []
    index = 0
    for opp_odds in opp_odds_list:
        opp_odds_list_copy = opp_odds_list.copy()
        opp_odds_list_copy.pop(index)
        other_prob = american_to_probability_average_multi(opp_odds, [odds] + opp_odds_list_copy)
        other_bets.append(other_prob * total_bet)
        index += 1
    return bet_1, other_bets

def even_split_bet_expected_return(odds_1, odds_2):
    bet_1, bet_2 = even_split_bet_amounts(odds_1, odds_2)
    profit_if_1_wins = profit_from_win(odds_1, bet_1) + bet_1
    profit_if_2_wins = profit_from_win(odds_2, bet_2) + bet_2
    assert abs(profit_if_1_wins - profit_if_2_wins) < 1e-6
    return profit_if_1_wins

def even_split_bet_expected_return_multi(odds, opp_odds_list):
    bet_1, other_bets = even_split_bet_amounts_multi(odds, opp_odds_list)
    profit_if_1_wins = profit_from_win(odds, bet_1) + bet_1
    return profit_if_1_wins

def get_bet_summary(odds_1, odds_2, total_bet=1):
    percent_probability = american_to_probability_average(odds_1, odds_2)
    opp_percent_probability = 1 - percent_probability
    bet_amount, bet_amount_opp = even_split_bet_amounts(odds_1, odds_2, total_bet)
    expected_return = even_split_bet_expected_return(odds_1, odds_2) * total_bet
    # return as JSON
    return {
        "percent_probability": percent_probability,
        "opp_percent_probability": opp_percent_probability,
        "bet_amount": bet_amount,
        "bet_amount_opp": bet_amount_opp,
        "expected_return": expected_return
    }

def get_bet_summary_multi(odds, opp_odds_list, total_bet=1):
    percent_probability = american_to_probability_average_multi(odds, opp_odds_list)
    bet_amount, other_bets = even_split_bet_amounts_multi(odds, opp_odds_list, total_bet)
    opp_percent_probabilities = [american_to_probability_average_multi(opp_odds, [odds] + opp_odds_list[:index] + opp_odds_list[index+1:]) for index, opp_odds in enumerate(opp_odds_list)]
    expected_return = even_split_bet_expected_return_multi(odds, opp_odds_list) * total_bet
    # return as JSON
    return {
        "percent_probability": percent_probability,
        "opp_percent_probabilities": opp_percent_probabilities,
        "bet_amount": bet_amount,
        "other_bets": other_bets,
        "expected_return": expected_return
    }