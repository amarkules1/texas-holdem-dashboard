# texas-holdem-dashboard

## Description

A webapp that helps you make decisions in a game of Texas Holdem Poker.
It currently tells you the probability of winning a hand based on the cards you have pre-flop.

## Setup

1. Assumes you have a database with the tables form the `schema` directory (assumes this table is populated based on scripts in [texas-holdem-notebooks](https://github.com/amarkules1/texas-holdem-notebooks)).
2. Assumes you have a .env file in the root project directory with the following variables:
    - `DATABASE_CONN_STRING`
3. Execute the `start.sh` script to start the app as a docker container.


## Development

Install dependencies: `pipenv install --dev`

run app: `pipenv run flask --app main:app run`

regen requirements.txt after adding a dependency: `pipenv lock -r > requirements.txt`

regenerate frontend assets (from `/texas-holdem-front-end`): `npm i && npm run build`
