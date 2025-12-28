from flask import Flask, request, redirect
import psycopg2
from flask_cors import CORS
import logging
from dotenv import load_dotenv, find_dotenv
import sqlalchemy
import os
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype
from texas_hold_em_utils.card import Card
from texas_hold_em_utils.preflop_stats_repository import PreflopStatsRepository
import texas_hold_em_utils.relative_ranking as rr
from texas_hold_em_utils.outs_counter import OutsMetrics

from game_tracking.game_tracker import GameTracker
from game_tracking.player_round_stats_repository import PlayerRoundStatsRepository
from betting_odds.odds_functions import get_bet_summary

# create console logger and file logger

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler1 = logging.StreamHandler()
handler1.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler1)
handler2 = logging.FileHandler('texas-holdem-dashboard.txt')
handler2.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler2)


app = Flask(__name__, static_folder='texas-holdem-frontend/dist', static_url_path='')
CORS(app)

load_dotenv()
db_conn_string = os.getenv("DATABASE_CONN_STRING")
db_conn = psycopg2.connect(db_conn_string)

_ = load_dotenv(find_dotenv())

preflop_stats_repo = PreflopStatsRepository()
player_round_stats_repo = PlayerRoundStatsRepository()
game_tracker = GameTracker(player_round_stats_repo=player_round_stats_repo)


@app.route('/')
def hello():
    return redirect("/index.html", code=302)


@app.route('/compare-hands', methods=['GET'])
def compare_hands():
    """
    :return: win rate for each hand in the request
    """
    hands = []
    community_cards = []
    for i in range(1, 12):
        if f'hand{i}' in request.args.keys():
            hand = request.args.get(f'hand{i}')
            cards = [Card().from_name(card) for card in hand.split(',')]
            hands.append(cards)
    if request.args.get('community_cards'):
        community_cards = [Card().from_name(card) for card in request.args.get('community_cards').split(',')]
    return rr.compare_hands(hands, community_cards=community_cards, sample_size=2000)



@app.route("/card-stats", methods=['GET'])
def card_stats():
    """
    :return: json with keys:
        preflop_win_rate,
        current_win_rate,
        percentile,
        sklansky,
        sklansky_position,
        modified_sklansky,
        modified_sklansky_position
    """
    card1 = Card().from_name(request.args.get('card1'))
    card2 = Card().from_name(request.args.get('card2'))
    player_count = request.args.get('player_count')

    community_cards = []
    # check if flop is provided
    if 'flop1' in request.args.keys():
        community_cards.append(Card().from_name(request.args.get('flop1')))
        community_cards.append(Card().from_name(request.args.get('flop2')))
        community_cards.append(Card().from_name(request.args.get('flop3')))
    # check if turn is provided
    if 'turn' in request.args.keys():
        community_cards.append(Card().from_name(request.args.get('turn')))
    # check if river is provided
    if 'river' in request.args.keys():
        community_cards.append(Card().from_name(request.args.get('river')))
    data = preflop_stats_repo.get_win_rate(card1.rank, card2.rank, card1.suit == card2.suit, player_count)
    data['preflop_win_rate'] = data['win_rate']

    hand_stats = rr.get_hand_rank_details([card1, card2], community_cards, int(player_count), 3000)
    data['current_win_rate'] = hand_stats['expected_win_rate']
    data['percentile'] = hand_stats['percentile']
    data['ideal_kelly_max'] = hand_stats['ideal_kelly_max']

    # Flask seems to convert the dict to a string, series.to_json() worked before so there you go)
    return pd.Series(data=data).to_json()

@app.route('/game-file', methods = ['POST'])
def success():
    f = request.files['file']
    for line in f.stream:
        game_tracker.parse_line(line.decode('utf-8'))
    game_tracker.save_player_round_summaries()
    return {'status': 'success'}

@app.route('/player-summaries', methods = ['GET'])
def player_summaries():
    df = player_round_stats_repo.get_player_summaries()
    df['preflop_fold_rate'] = df['preflop_fold_count'] / df['game_count']
    df['preturn_fold_rate'] = df['preturn_fold_count'] / df['game_count']
    df['preriver_fold_rate'] = df['preriver_fold_count'] / df['game_count']
    df['preshowdown_fold_rate'] = df['preshowdown_fold_count'] / df['game_count']
    df['raise_rate'] = df['total_raise_count'] / df['game_count']
    df['call_rate'] = df['total_call_count'] / df['game_count']
    df['check_rate'] = df['check_count'] / df['game_count']
    df['profit_loss'] = df['total_won'] - df['total_paid_in']
    df['profit_loss_per_game'] = df['profit_loss'] / df['game_count']
    df['profit_loss_bb'] = df['total_won_bb'] - df['total_paid_in_bb']
    df['profit_loss_per_game_bb'] = df['profit_loss_bb'] / df['game_count']
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            df[f"{col}_z_score"] = (df[col] - df[col].mean()) / df[col].std()
    # folds late = bluffable
    df['bluffable_score'] = (((df['preriver_fold_rate'] + df['preshowdown_fold_rate']) / 2) - (df['preflop_fold_rate']))
    df['bluffable_score_z_score'] = (df['bluffable_score'] - df['bluffable_score'].mean()) / df['bluffable_score'].std()
    # limper = low fold rates, low raise rate
    df['limper_score'] = -1 * (df['raise_rate'] + ((df['preflop_fold_rate'] + df['preturn_fold_rate'] + df['preriver_fold_rate'] + df['preshowdown_fold_rate']) / 4))
    df['limper_score_z_score'] = (df['limper_score'] - df['limper_score'].mean()) / df['limper_score'].std()
    # aggressive = high raise rate, low fold rates
    df['aggressive_score'] = df['raise_rate'] - ((df['preflop_fold_rate'] + df['preturn_fold_rate'] + df['preriver_fold_rate'] + df['preshowdown_fold_rate']) / 4)
    df['aggressive_score_z_score'] = (df['aggressive_score'] - df['aggressive_score'].mean()) / df['aggressive_score'].std()

    df.sort_values('last_timestamp', ascending=False, inplace=True)
    return df.to_json(orient='records')

@app.route('/all-player-outs', methods=['GET'])
def all_player_outs():
    hands_orig = request.args.get('hands')
    hands = [hand.split(",") for hand in hands_orig.split("/")]
    hands = [[Card().from_name(card) for card in hand] for hand in hands]
    community_cards_orig = request.args.get('community_cards')
    community_cards = [Card().from_name(card) for card in community_cards_orig.split(",")]
    outs_metrics = OutsMetrics(hands, community_cards)
    return outs_metrics.to_json()

@app.route('/blackjack-basic-strategy', methods=['GET'])
def blackjack_basic_strategy():
    where_clauses = []
    if 'dealer_hit_soft_17' in request.args:
        val = str(request.args.get('dealer_hit_soft_17')).lower() == 'true'
        where_clauses.append(f"dealer_hit_soft_17 = {val}")

    if 'double_after_split' in request.args:
        val = str(request.args.get('double_after_split')).lower() == 'true'
        where_clauses.append(f"double_after_split = {val}")

    if 'blackjack_pays' in request.args:
        val = request.args.get('blackjack_pays', type=float)
        where_clauses.append(f"blackjack_pays = {val}")

    query = "SELECT * FROM blackjack_odds"
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    return pd.read_sql(query, db_conn).to_json(orient='records')
    

@app.route('/bet-summary', methods=['GET'])
def bet_summary():
    """
    Returns a summary of betting odds.
    Query parameters:
    - odds_1: int (required) - American odds for the first outcome
    - odds_2: int (required) - American odds for the second outcome
    - total_bet: float (optional, default=1) - Total amount to bet
    """
    odds_1 = request.args.get('odds_1', type=int)
    odds_2 = request.args.get('odds_2', type=int)
    total_bet = request.args.get('total_bet', default=1, type=float)
    
    if odds_1 is None or odds_2 is None:
        return {'error': 'odds_1 and odds_2 are required parameters'}, 400
        
    return get_bet_summary(odds_1, odds_2, total_bet)
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)
