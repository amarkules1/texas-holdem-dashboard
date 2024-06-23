from flask import Flask, request, redirect
from flask_cors import CORS
import logging
from dotenv import load_dotenv, find_dotenv
import sqlalchemy
import os
import pandas as pd
import texas_hold_em_utils.card as card


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

_ = load_dotenv(find_dotenv())


@app.route('/')
def hello():
    return redirect("/index.html", code=302)


@app.route("/card-stats", methods=['GET'])
def card_stats():
    card1 = card.Card().from_name(request.args.get('card1'))
    card2 = card.Card().from_name(request.args.get('card2'))
    player_count = request.args.get('player_count')

    conn = get_connection()
    data = pd.read_sql(sqlalchemy.sql.text(f"select * from poker.win_rates where player_count = {player_count} and "
                                           f"card_1_rank = '{card1.rank}' and card_2_rank = '{card2.rank}' "
                                           f"and {'' if card1.suit == card2.suit else 'not '}suited"), conn)
    conn.commit()
    conn.close()
    return data.iloc[0].to_json()


def get_connection():
    return sqlalchemy.create_engine(os.getenv("SUPABASE_CONN_STRING")).connect()


if __name__ == '__main__':
    app.run(port=5003, debug=True)
