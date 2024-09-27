<template>
    <div class="cardsDisplay">
        <div class="cards">
            <div v-for="card in cards" :key="card.rank + card.suit" class="card">
                <img class="cardImage" :src="require(`../assets/cards/${card.suit}_${card.rank}.svg`)" alt="card" />
            </div>
        </div>
    </div>
    <div class="cardSelectionHolder">
        <CardSelector :disabledCards="cards" @selectCard="(rank, suit) => selectCard(rank, suit)" />
    </div>
</template>

<script>
import CardSelector from './CardSelector.vue'

export default {
    name: 'CardStatsContainer',
    components: {
        CardSelector
    },
    data() {
        return {
            holeCards: [],
            communityCards: [],
            cards: []
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