<template>
    <div class="container">
        <div class="row">
            <div class="col-4">
                <button @click="backButton" class="btn btn-info back-btn">Back</button>
            </div>
            <div class="col-4">
                <div class="playerCtInput">
                    <label for="playerCount">Player Count: </label>
                    <select v-model="playerCount" @change="updatePlayerList" class="form-select playerCtSelect">
                        <option v-for="count in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]" :key="count" :value="count">{{count }}</option>
                    </select>
                </div>
            </div>
            <div class="col-4">
                <button @click="reset" class="btn btn-warning reset-btn">Reset</button>
            </div>
        </div>
    </div>
    <div>
        <div class="playerCards" v-if="!loadingStats">
        <div v-for="playerNum in [...Array(playersCards.length).keys()]" :key="playerNum" class="playerCardsHolder">
            <h4 class="playerCardsTitle">{{getPlayerTitle(playerNum)}}</h4>
            <div v-for="i in [0,1]" :key="i" class="playingCard" >
                    <div class="noshow" v-if="i < playersCards[playerNum].length">
                        <img class="cardImage" :src="require(`../assets/cards/${playersCards[playerNum][i].suit}_${playersCards[playerNum][i].rank}.svg`)" alt="card" rel="preload"/>
                    </div>
                    <div class="noshow" v-else>
                        <img class="cardImage" :src="require(`../assets/cards/gray.svg`)" alt="card" rel="preload"/>
                    </div> 
                </div>
        </div>
        </div>
        <div class="communityCards">
            <h4>Community Cards</h4>
                <div v-for="i in [0,1,2,3,4]" :key="i" class="playingCard" >
                    <div class="noshow" v-if="i < communityCards.length">
                        <img class="cardImage" :src="require(`../assets/cards/${communityCards[i].suit}_${communityCards[i].rank}.svg`)" alt="card" />
                    </div>
                    <div v-else>
                        <img class="cardImage" :src="require(`../assets/cards/gray.svg`)" alt="card" />
                    </div> 
                </div>
        </div>

        <div class="cardSelectionHolder" v-if="communityCards.length < 5">
            <CardSelector :disabledCards="cards"
                @selectCard="(rank, suit) => selectCard(rank, suit)" />
        </div>
        <div v-if="loadingStats">
            <div class="spinner-border" role="status">
                <span class="sr-only">Loading...</span>
            </div>
        </div>
    </div>
</template>

<script>
import CardSelector from './CardSelector.vue'
import axios from 'axios'

export default {
    name: 'HandComparison',
    components: {
        CardSelector,
    },
    data() {
        return {
            playersCards: [[],[]],
            communityCards: [],
            cards: [],
            playerCount: 2,
            perf: null,
            loadingStats: false
        }
    },
    methods: {
        selectCard(rank, suit) {
            // insert to the first player with less than 2 cards
            for (let i = 0; i < this.playerCount; i++) {
                if (this.playersCards[i].length < 2) {
                    this.playersCards[i].push({ "rank": rank, "suit": suit })
                    this.cards.push({ "rank": rank, "suit": suit })
                    this.getHandPerformance()
                    return
                }
            }
            if (this.communityCards.length < 5) {
                this.communityCards.push({ "rank": rank, "suit": suit })
                this.cards.push({ "rank": rank, "suit": suit })
                this.getHandPerformance()
            }
        },

        getPlayerTitle(playerNumber) {
            let retVal = "Player " + (playerNumber + 1) 
            if (this.perf && this.perf.length > playerNumber) {
                retVal += ` (${(this.perf[playerNumber] * 100).toFixed(3)}%)`
            }
            return retVal
        },

        backButton() {
            if (this.communityCards.length > 0) {
                this.communityCards.pop()
                this.cards.pop()
                this.getHandPerformance()
                return
            }
            // iterate through players in reverse order
            for (let i = this.playerCount - 1; i >= 0; i--) {
                if (this.playersCards[i].length > 0) {
                    this.playersCards[i].pop()
                    this.cards.pop()
                    this.getHandPerformance()
                    return
                }
            }
        },

        reset() {
            this.cards = []
            this.holeCards = []
            this.communityCards = []
            this.perf = null
        },

        async getHandPerformance() {
            this.perf = null
            for (let i = 0; i < this.playerCount; i++) {
                if (this.playersCards[i].length < 2) {
                    return
                }
            }
            this.loadingStats = true;
            let queryString = process.env.VUE_APP_REST_ENDPOINT + "/compare-hands?"
            for (let i = 0; i < this.playerCount; i++) {
                queryString += `hand${i + 1}=${this.getCardNameForBackend(this.playersCards[i][0].rank, this.playersCards[i][0].suit)},` + 
                                            `${this.getCardNameForBackend(this.playersCards[i][1].rank, this.playersCards[i][1].suit)}&`
            }
            if (this.communityCards.length > 2) {
                queryString += "community_cards="
                for (let i = 0; i < this.communityCards.length; i++) {
                    queryString += `${this.getCardNameForBackend(this.communityCards[i].rank, this.communityCards[i].suit)},`
                }
            }

            queryString = queryString.slice(0, -1)
            
            const response = await axios.get(queryString)
            this.perf = response.data
            this.loadingStats = false
        },

        updatePlayerList() {
            this.loadingStats = true
            
            this.communityCards = []
            if (this.playerCount > this.playersCards.length) {
                let prevPlayerCount = this.playersCards.length
                for (let i = 0; i < this.playerCount - prevPlayerCount; i++) {
                    this.playersCards.push([])
                }
            }
            if (this.playerCount < this.playersCards.length) {
                this.playersCards = this.playersCards.slice(0, this.playerCount)
            }
            
            this.getHandPerformance()
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
.playingCard {
    display: inline-block;
    margin: 10px;
}

.cardsDisplay {
    /* height:160px; */
}


.holeCards {
    display: inline-block;
    width: 300px;
}

.communityCards {
    display: inline-block;
    max-width: 500px;
}

.cardImage {
    height:80px;
    margin: 0px;
    border: 1px solid black;
    border-radius: 4px;
}

.playerCardsHolder {
    display: flex;
    margin: auto;
    max-width: 300px;
}

.playerCardsTitle {
    margin: auto;
}


</style>