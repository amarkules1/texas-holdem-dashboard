<template>
    <SelectedCards :holeCards="holeCards" :communityCards="communityCards" />
    <div class="buttonBar">
      <button @click="backButton">Back</button>
      <button @click="reset">Reset</button>
    </div>
    <div class="cardSelectionHolder" v-if="cards.length < 7">
        <CardSelector :cardToSelect="getCardName()" :disabledCards="cards" @selectCard="(rank, suit) => selectCard(rank, suit)" />
    </div>
</template>

<script>
import CardSelector from './CardSelector.vue'
import SelectedCards from './SelectedCards.vue'

export default {
    name: 'CardStatsContainer',
    components: {
        CardSelector,
        SelectedCards
    },
    data() {
        return {
            holeCards: [],
            communityCards: [],
            cards: [],
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
        },
        reset () {
            this.cards = []
            this.holeCards = []
            this.communityCards = []
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
}
</style>