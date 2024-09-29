<template>
    <div class="cardsDisplay">
        <div class="cards">
            <div class="holeCards">
                <h2>Hole Cards</h2>
                <div v-for="card in holeCards" :key="card.rank + card.suit" class="card">
                    <img class="cardImage" :src="require(`../assets/cards/${card.suit}_${card.rank}.svg`)" alt="card" />
                </div>
            </div>
            <div class="communityCards">
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

.cardDisplay {
    display: flex;
    justify-content: center;
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