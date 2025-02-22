<template>
  <div class="cardSelector">
    <h3>Select the {{ cardToSelect }}</h3>
    <div v-for="suit in suits" :key="suit" class="suitRow">
      <div 
        v-for="rank in ranks" 
        :key="rank" 
        :class="{ card: true, 
                  disabled: disabledCards.some(card => card.rank == rank && card.suit == suit) }"
        @click="selectCard(rank, suit)">
        <img class="cardImage" :src="require(`../assets/cards/${suit}_${rank}.svg`)" alt="card" rel="preload"/>
      </div>
    </div>
  </div>
</template>


<script>

export default {
  name: 'CardSelector',
  data() {
    return {
      rank: "",
      suit: "",
      ranks: ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace'],
      suits: ['clubs', 'diamonds', 'hearts', 'spades']
    }
  },
  props: {
    "disabledCards": {
      type: Array,
      default: () => []
    },
    "cardToSelect": {
      type: String,
      default: ""
    }
  },
  methods: {
    selectCard(rank, suit) {
      if (this.disabledCards.some(card => card.rank == rank && card.suit == suit)) {
        return
      }
      this.rank = rank;
      this.suit = suit;
      this.$emit('selectCard', rank, suit)
    },
  },
  emits: ['selectCard']
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.card {
  display: inline-block;
  margin: 5px 0.25%;
  width: 4%;
  border: 1px solid black;
  min-width: 28px;
}

.disabled {
  opacity: 35%;
}

.cardImage {
  width: 100%;
}
.cardSelector {
  margin-top: 20px;
}
</style>
