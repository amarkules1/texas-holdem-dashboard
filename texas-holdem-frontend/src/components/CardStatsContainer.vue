<template>
    <div class="container">
        <div class="row">
            <div class="col-4">
                <button @click="backButton" class="btn btn-info back-btn">Back</button>
            </div>
            <div class="col-4">
                <div class="playerCtInput">
                    <label for="playerCount">Player Count: </label>
                    <select v-model="playerCount" @change="getHandPerformance" class="form-select playerCtSelect">
                        <option v-for="count in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]" :key="count" :value="count">{{
                            count }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="col-4">
                <button @click="reset" class="btn btn-warning reset-btn">Reset</button>
                <button @click="showInfo = !showInfo" class="btn btn-secondary info-btn">
                    <FontAwesomeIcon :icon="faInfoCircle" />
                </button>
            </div>
        </div>
    </div>
    <div>

        <SelectedCards :holeCards="holeCards" :communityCards="communityCards" />
        <div v-if="cards.length >= 2 && !loadingStats">
            <StatsDisplay :perf="perf" :card-count="cards.length" />
        </div>



        <div class="cardSelectionHolder" v-if="cards.length < 7 && !loadingStats">
            <CardSelector :cardToSelect="getCardName()" :disabledCards="cards"
                @selectCard="(rank, suit) => selectCard(rank, suit)" />
        </div>
        <div v-if="loadingStats">
            <div class="spinner-border" role="status">
                <span class="sr-only">Loading...</span>
            </div>
        </div>
    </div>
    <div class="info-bg" v-if="showInfo">
        <div class="info-container">
            <div class="info-close" @click="showInfo = !showInfo">
                <FontAwesomeIcon :icon="faTimes" size="lg" />
            </div>
            <div class="info-text">
                <h3>Instructions</h3>
                <p>This dashboard provides statistics about your poker hand at any point in the
                    game.
                    <br />
                    To see stats about a particular scenario, select your hole (hand) cards and any known community
                    cards.
                    The following statistics will be displayed:
                </p>
                <ul class="info-descriptions list-group">
                    <li class="list-group-item">
                        <strong>Current Win Rate:</strong> Expected win rate against (as a proportion) random hands,
                        based on the number of players, your hand, and any known community cards. This win rate assumes
                        other players have a random hand, which may become a less accurate estimate as the game
                        progresses
                        and players with worse hands fold, but it still gives you an idea of the relative strength of
                        your hand.
                    </li>
                    <li class="list-group-item">
                        <strong>Kelly Criterion:</strong> The percentage of your chips that you should bet based on the
                        strength of your hand.
                        The <a href="https://en.wikipedia.org/wiki/Kelly_criterion">Kelly Criterion</a> is based on the
                        number of players and the current win rate, so the same caveats apply. You may find
                        that a smaller amount (e.g. 1/2 or 1/3 of the Kelly Criterion) is a better bet.
                    </li>
                    <li class="list-group-item">
                        <strong>Percentile:</strong> Relative ranking (as a percentile) against all other hands at the
                        current point.
                    </li>
                    <li class="list-group-item">
                        <strong>Sklansky Rank:</strong> Number from 1 to 9 indicating the strength of your hand
                        pre-flop, based on <a
                            href="https://en.wikipedia.org/wiki/Texas_hold_%27em_starting_hands#Sklansky_hand_groups">Sklansky
                            Hand Groups</a>.
                    </li>
                    <li class="list-group-item">
                        <strong>Sklansky Position:</strong> Description of the Sklansky hand rank, the position and
                        scenario in which you should play it.
                    </li>
                </ul>
                <br />
                <p>Author: <a href="http://marqless.xyz">Alex Markules</a></p>
            </div>
        </div>
    </div>
</template>

<script>
import CardSelector from './CardSelector.vue'
import SelectedCards from './SelectedCards.vue'
import StatsDisplay from './StatsDisplay.vue'
import axios from 'axios'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faInfoCircle, faTimes } from '@fortawesome/free-solid-svg-icons'

export default {
    name: 'CardStatsContainer',
    components: {
        CardSelector,
        SelectedCards,
        StatsDisplay,
        FontAwesomeIcon
    },
    data() {
        return {
            holeCards: [],
            communityCards: [],
            cards: [],
            playerCount: 2,
            perf: null,
            selections: ["First Hole Card",
                "Second Hole Card",
                "First Flop Card",
                "Second Flop Card",
                "Third Flop Card",
                "Turn Card",
                "River Card"],
            loadingStats: false,
            showInfo: false,
            faInfoCircle,
            faTimes
        }
    },
    methods: {
        selectCard(rank, suit) {
            if (this.holeCards.length < 2) {
                this.holeCards.push({ "rank": rank, "suit": suit })
            } else if (this.communityCards.length < 5) {
                this.communityCards.push({ "rank": rank, "suit": suit })
            }
            this.cards.push({ "rank": rank, "suit": suit })
            this.getHandPerformance()
        },

        getCardName() {
            return this.selections[this.cards.length]
        },

        backButton() {
            if (this.cards.length > 0) {
                this.cards.pop()
            }
            if (this.communityCards.length > 0) {
                this.communityCards.pop()
            } else if (this.holeCards.length > 0) {
                this.holeCards.pop()
            }
            this.perf = null
            this.getHandPerformance()
        },

        reset() {
            this.cards = []
            this.holeCards = []
            this.communityCards = []
            this.perf = null
        },

        async getHandPerformance() {
            if (this.cards.length < 2) {
                return
            }
            let queryString = process.env.VUE_APP_REST_ENDPOINT + "/card-stats?"
            queryString += `card1=${this.getCardNameForBackend(this.cards[0].rank, this.cards[0].suit)}`
            queryString += `&card2=${this.getCardNameForBackend(this.cards[1].rank, this.cards[1].suit)}`

            if (this.communityCards.length > 2) {
                queryString += `&flop1=${this.getCardNameForBackend(this.communityCards[0].rank, this.communityCards[0].suit)}`
                queryString += `&flop2=${this.getCardNameForBackend(this.communityCards[1].rank, this.communityCards[1].suit)}`
                queryString += `&flop3=${this.getCardNameForBackend(this.communityCards[2].rank, this.communityCards[2].suit)}`
            }

            if (this.communityCards.length > 3) {
                queryString += `&turn=${this.getCardNameForBackend(this.communityCards[3].rank, this.communityCards[3].suit)}`
            }

            if (this.communityCards.length > 4) {
                queryString += `&river=${this.getCardNameForBackend(this.communityCards[4].rank, this.communityCards[4].suit)}`
            }

            queryString += `&player_count=${this.playerCount}`
            this.loadingStats = true
            const response = await axios.get(queryString)
            this.perf = response.data
            this.loadingStats = false
        },

        getCardNameForBackend(rank, suit) {
            let rankName = rank;
            if (rankName.length > 2) {
                rankName = rankName[0].toUpperCase()
            }
            let suitName = suit.charAt(0).toUpperCase() + suit.slice(1);
            return `${rankName} of ${suitName}`
        }
    }
}
</script>

<style scoped>
.buttonBar {
    height: 50px;
}

.back-btn {
    margin: 5%;
}

.reset-btn {
    margin: 5%;
}

.playerCtSelect {
    max-width: 100px;
    margin: auto;
}

.info-btn {
    margin-left: 10px;
}

.info-bg {
    display: block;
    /* Hidden by default */
    position: fixed;
    /* Stay in place */
    z-index: 1;
    /* Sit on top */
    left: 0;
    top: 0;
    width: 100%;
    /* Full width */
    height: 100%;
    /* Full height */
    overflow: auto;
    /* Enable scroll if needed */
    background-color: rgb(0, 0, 0);
    /* Fallback color */
    background-color: rgba(0, 0, 0, 0.4);
    /* Black w/ opacity */
}

.info-container {
    border: 3px solid #fff;
    border-radius: 10px;
    width: 70%;
    background-color: #000;
    position: fixed;
    top: 25%;
    left: 15%;
    opacity: 1;
    z-index: 1000;
}

.info-close {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 24px;
    color: #fff;
    cursor: pointer;
    transition: opacity 0.3s;
}

.info-text {
    margin: 40px 10px 10px 10px;
    padding: 20px;
    color: #fff;
    overflow: auto;
    max-height: 400px;
}
</style>