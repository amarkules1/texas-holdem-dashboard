<template>
    <div class="cardsDisplay">
        <div class="cards">
            <div class="holeCards" >
                <h4>Hole Cards</h4>
                <div v-for="i in [0,1]" :key="i" class="playingCard" >
                    <div class="noshow" v-if="i < holeCards.length">
                        <img class="cardImage" :src="require(`../assets/cards/${holeCards[i].suit}_${holeCards[i].rank}.svg`)" alt="card" />
                    </div>
                    <div class="noshow" v-else>
                        <img class="cardImage" :src="require(`../assets/cards/gray.svg`)" alt="card" />
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

</style>