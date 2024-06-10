from flask import Flask, request, redirect
from flask_cors import CORS
import logging
from dotenv import load_dotenv, find_dotenv
import sqlalchemy
import os
import pandas as pd


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
    card1 = request.args.get('card1')
    card2 = request.args.get('card2')
    conn = get_connection()
    data = pd.read_sql(sqlalchemy.sql.text(f"select * from poker.two_player_game_odds where card_1 = '{card1}' and card_2 = '{card2}'"), conn)
    conn.commit()
    conn.close()
    return data.iloc[0].to_json()


def get_connection():
    return sqlalchemy.create_engine(os.getenv("SUPABASE_CONN_STRING")).connect()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
