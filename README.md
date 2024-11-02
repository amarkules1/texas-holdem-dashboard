# texas-holdem-dashboard

## Description

A webapp that helps you make decisions in a game of Texas Holdem Poker.
It currently tells you the probability of winning a hand based on the cards you have pre-flop.


## Development

Install dependencies: `pipenv install --dev`

run app: `pipenv run flask --app main:app run`

regen requirements.txt after adding a dependency: `pipenv lock -r > requirements.txt`

regenerate frontend assets (from `/texas-holdem-front-end`): `npm i && npm run build`
