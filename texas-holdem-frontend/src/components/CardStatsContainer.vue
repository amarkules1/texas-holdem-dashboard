<template>
    <SelectedCards :holeCards="holeCards" :communityCards="communityCards" />
    <div v-if="perf">
        <StatsDisplay :perf="perf" />
    </div>
    <div>
        <label for="playerCount">Player Count: </label>
        <select v-model="playerCount" @change="getHandPerformance">
      <option v-for="count in [2,3,4,5,6,7,8,9,10,11,12]" :key="count" :value="count">{{ count }}</option>
    </select>
    </div>
    
    <div class="buttonBar">
        <button @click="backButton">Back</button>
        <button @click="reset">Reset</button>
    </div>
    <div class="cardSelectionHolder" v-if="cards.length < 7">
        <CardSelector :cardToSelect="getCardName()" :disabledCards="cards"
            @selectCard="(rank, suit) => selectCard(rank, suit)" />
    </div>
</template>

<script>
import CardSelector from './CardSelector.vue'
import SelectedCards from './SelectedCards.vue'
import StatsDisplay from './StatsDisplay.vue'
import axios from 'axios'

export default {
    name: 'CardStatsContainer',
    components: {
        CardSelector,
        SelectedCards,
        StatsDisplay
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
                "River Card"]
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
            let queryString = "/card-stats?"
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

            const response = await axios.get(queryString)
            this.perf = response.data
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
.card {
    display: inline-block;
    margin: 5px 10px;
    width: 10%;
    border: 1px solid black;
}

.cardDisplay {
    display: flex;
    justify-content: center;
}

.cardImage {
    width: 100%;
}</style>