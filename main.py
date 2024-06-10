from flask import Flask, redirect
from flask_cors import CORS
import logging
from dotenv import load_dotenv, find_dotenv


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
def daily_price_hist():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
