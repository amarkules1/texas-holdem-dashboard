<template>
  <div class="selectors">
    <h1>{{ msg }}</h1>
    <h2>First Card</h2>
    <div class="cardSelector">
      <div v-for="suit in suits" :key="suit" class="suitRow">
        <div v-for="rank in ranks" :key="rank" :class="{card: true, selected: firstRank == rank && firstSuit == suit}" @click="selectFirstCard(rank, suit)">
          <img class="cardImage" :src="require(`../assets/cards/${suit}_${rank}.svg`)" alt="card" />
        </div>
      </div>
    </div>
    <h2>Second Card</h2>
    <div class="cardSelector" id="cardSelector2">
      <div v-for="suit in suits" :key="suit" class="suitRow">
        <div v-for="rank in ranks" :key="rank" :class="{card: true, selected: secondRank == rank && secondSuit == suit}" @click="selectSecondCard(rank, suit)">
          <img class="cardImage" :src="require(`../assets/cards/${suit}_${rank}.svg`)" alt="card" />
        </div>
      </div>
    </div>
  </div>
  <div class="statsContainer">
  <div class="stats">
    <h3>Hand Performance</h3>
    <ul>
      <li>
        Win Rate: {{ perf.win_rate ? perf.win_rate.toFixed(3) : "N/A" }}
      </li>
      <li>
        Percentile: {{ perf.percentile ? perf.percentile.toFixed(3) : "N/A" }}%
      </li>
      <li>
        Sklansky Rank: {{ perf.sklansky }}
      </li>
      <li>
        Sklansky Playability: <strong>{{ perf.sklansky_position }}</strong>
      </li>
      <li>
        Modified Sklansky Rank: {{ perf.modified_sklansky }}
      </li>
      <li>
        Modified Sklansky Playability: <strong>{{ perf.modified_sklansky_position }}</strong>
      </li>
    </ul>
  </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HoleCards',
  data() {
    return {
      firstRank: "",
      firstSuit: "",
      secondRank: "",
      secondSuit: "",
      ranks: ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace'],
      suits: ['clubs', 'diamonds', 'hearts', 'spades'],
      perf: {}
    }
  },
  methods: {
    selectFirstCard(rank, suit) {
      this.firstRank = rank;
      this.firstSuit = suit;
      if (this.secondRank && this.secondSuit) {
        this.getHandPerformance()
      }
    },
    selectSecondCard(rank, suit) {
      this.secondRank = rank;
      this.secondSuit = suit;
      if (this.firstRank && this.firstSuit) {
        this.getHandPerformance()
      }
    },
    async getHandPerformance() {
      let firstCardRank = this.firstRank
      let secondCardRank = this.secondRank
      if (firstCardRank.length > 2) {
        firstCardRank = firstCardRank[0].toUpperCase()
      }
      if (secondCardRank.length > 2) {
        secondCardRank = secondCardRank[0].toUpperCase()
      }
      firstCardRank += ` of ${this.firstSuit.charAt(0).toUpperCase() + this.firstSuit.slice(1)}`
      secondCardRank += ` of ${this.secondSuit.charAt(0).toUpperCase() + this.secondSuit.slice(1)}`

      const response = await axios.get(`http://localhost:5000/card-stats?card1=${firstCardRank}&card2=${secondCardRank}`)
      this.perf = response.data
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

.card {
  display: inline-block;
  margin: 5px 10px;
  width: 4%;
  border: 1px solid black;
}

.selected {
  border: 2px solid red;
}

.cardImage {
  width: 100%;
}
.statsContainer {
    position: fixed;
    top: 0;
    left: 0;
    height: 130px;
    z-index: 999;
    background-color: white;
    width: 100%;
}

.stats {
    width: 100%;
}

.selectors {
    height: 90%;
    overflow-y: scroll;
    position: fixed;
    top: 130px;
}

#cardSelector2 {
    margin-bottom: 50px;
}
</style>
