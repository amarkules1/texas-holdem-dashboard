<template>
    <div class="cardsDisplay">
        <div class="cards">
            <div class="holeCards" v-if="holeCards.length > 0">
                <h2>Hole Cards</h2>
                <div v-for="card in holeCards" :key="card.rank + card.suit" class="card">
                    <img class="cardImage" :src="require(`../assets/cards/${card.suit}_${card.rank}.svg`)" alt="card" />
                </div>
            </div>
            <div class="communityCards" v-if="communityCards.length > 0">
                <h2>Community Cards</h2>
                <div v-for="card in communityCards" :key="card.rank + card.suit" class="card">
                    <img class="cardImage" :src="require(`../assets/cards/${card.suit}_${card.rank}.svg`)" alt="card" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'SelectedCards',
    props: {
        "holeCards": {
            type: Array,
            default: () => []
        },
        "communityCards": {
            type: Array,
            default: () => []
        }
    },
}
</script>

<style scoped>
.card {
    display: inline-block;
    margin: 5px 10px;
    width: 125px;
}

.cardsDisplay {
    height:260px;
}

.cardImage {
    width: 100%;
}

.holeCards {
    display: inline-block;
    width: 33%;
}

.communityCards {
    display: inline-block;
    width: 50%;
}
</style>