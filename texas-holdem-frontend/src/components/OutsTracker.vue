<template>
  <div class="outs-tracker container">
    <div class="row">
      <div class="col-4">
        <button @click="backButton" class="btn btn-info back-btn">Back</button>
      </div>
      <div class="col-4">
        <div class="playerCtInput">
          <label for="playerCount">Player Count: </label>
          <select v-model="playerCount" @change="updatePlayerList" class="form-select playerCtSelect">
            <option v-for="count in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]" :key="count" :value="count">{{ count }}</option>
          </select>
        </div>
      </div>
      <div class="col-4">
        <button @click="reset" class="btn btn-warning reset-btn">Reset</button>
      </div>
    </div>
    <div>
      <div class="playerCards" v-if="!loadingStats">
        <div v-for="playerNum in [...Array(playersCards.length).keys()]" :key="playerNum" class="playerCardsHolder">
          <h4 class="playerCardsTitle">{{ getPlayerTitle(playerNum) }}</h4>
          <div v-for="i in [0,1]" :key="i" class="playingCard">
            <div class="noshow" v-if="i < playersCards[playerNum].length">
              <img class="cardImage" :src="require(`../assets/cards/${playersCards[playerNum][i].suit}_${playersCards[playerNum][i].rank}.svg`)" alt="card" rel="preload"/>
            </div>
            <div class="noshow" v-else>
              <img class="cardImage" :src="require(`../assets/cards/gray.svg`)" alt="card" rel="preload"/>
            </div>
          </div>
          <div class="outsDisplay">
            <span v-if="outs && outs[playerNum] !== undefined && totalCombos">
              Outs: <b>{{ outs[playerNum].length }}</b>/{{ totalCombos }} ({{ ((outs[playerNum].length / totalCombos) * 100).toFixed(1) }}%)
            </span>
            <span v-else>Outs: N/A</span>
          </div>
        </div>
      </div>
      <div class="communityCards">
        <h4>Community Cards</h4>
        <div v-for="i in [0,1,2,3,4]" :key="i" class="playingCard">
          <div class="noshow" v-if="i < communityCards.length">
            <img class="cardImage" :src="require(`../assets/cards/${communityCards[i].suit}_${communityCards[i].rank}.svg`)" alt="card" />
          </div>
          <div v-else>
            <img class="cardImage" :src="require(`../assets/cards/gray.svg`)" alt="card" />
          </div>
        </div>
      </div>
      <div class="cardSelectionHolder" v-if="communityCards.length < 5">
        <CardSelector :disabledCards="cards" cardToSelect="Next Card"
                      @selectCard="(rank, suit) => selectCard(rank, suit)" />
      </div>
      <div v-if="loadingStats">
        <div class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CardSelector from './CardSelector.vue'
import axios from 'axios'

export default {
  name: 'OutsTracker',
  components: {
    CardSelector
  },
  data() {
    return {
      playersCards: [[], []],
      communityCards: [],
      cards: [],
      playerCount: 2,
      outs: null,
      totalCombos: null,
      loadingStats: false
    }
  },
  methods: {
    selectCard(rank, suit) {
      // Insert to the first player with less than 2 cards
      for (let i = 0; i < this.playerCount; i++) {
        if (this.playersCards[i].length < 2) {
          this.playersCards[i].push({ rank, suit })
          this.cards.push({ rank, suit })
          this.getOuts()
          return
        }
      }
      // If all players have 2 cards, add to community
      if (this.communityCards.length < 5) {
        this.communityCards.push({ rank, suit })
        this.cards.push({ rank, suit })
        this.getOuts()
      }
    },
    getPlayerTitle(playerNumber) {
      return `Player ${playerNumber + 1}`
    },
    backButton() {
      if (this.cards.length > 0) {
        const last = this.cards.pop()
        // Remove from players or community
        for (let i = 0; i < this.playerCount; i++) {
          if (this.playersCards[i].length > 0 && this.playersCards[i][this.playersCards[i].length - 1].rank === last.rank && this.playersCards[i][this.playersCards[i].length - 1].suit === last.suit) {
            this.playersCards[i].pop()
            this.getOuts()
            return
          }
        }
        if (this.communityCards.length > 0 && this.communityCards[this.communityCards.length - 1].rank === last.rank && this.communityCards[this.communityCards.length - 1].suit === last.suit) {
          this.communityCards.pop()
          this.getOuts()
        }
      }
    },
    reset() {
      this.cards = []
      this.playersCards = Array.from({ length: this.playerCount }, () => [])
      this.communityCards = []
      this.outs = null
    },
    updatePlayerList() {
      // Adjust playersCards size
      if (this.playerCount > this.playersCards.length) {
        for (let i = this.playersCards.length; i < this.playerCount; i++) {
          this.playersCards.push([])
        }
      } else if (this.playerCount < this.playersCards.length) {
        this.playersCards = this.playersCards.slice(0, this.playerCount)
      }
      this.reset()
    },
    getCardNameForBackend(rank, suit) {
      let rankName = rank
      if (rankName.length > 2) {
        rankName = rankName[0].toUpperCase()
      }
      let suitName = suit.charAt(0).toUpperCase() + suit.slice(1)
      return `${rankName} of ${suitName}`
    },
    async getOuts() {
      if (this.playersCards.some(p => p.length < 2) || this.communityCards.length < 3) {
        this.outs = null
        this.totalCombos = null
        return
      }
      // Compute total combinations of remaining cards for remaining community slots
      const totalCards = 52
      const usedCards = this.playersCards.flat().length + this.communityCards.length
      const remainingCards = totalCards - usedCards
      const slotsLeft = 5 - this.communityCards.length
      let totalCombos = 1
      for (let i = 0; i < slotsLeft; i++) {
        totalCombos *= (remainingCards - i)
      }
      this.totalCombos = slotsLeft > 0 ? totalCombos : 1
      this.loadingStats = true
      // Prepare hands and community for backend
      const hands = this.playersCards.map(
        hand => hand.map(card => this.getCardNameForBackend(card.rank, card.suit)).join(",")
      ).join("/")
      const community = this.communityCards.map(card => this.getCardNameForBackend(card.rank, card.suit)).join(",")
      try {
        const response = await axios.get(`${process.env.VUE_APP_REST_ENDPOINT}/all-player-outs?hands=${hands}&community_cards=${community}`)
        // Expecting response to be { outs: [numOutsForPlayer1, numOutsForPlayer2, ...] }
        this.outs = response.data.outs
      } catch (e) {
        this.outs = null
      }
      this.loadingStats = false
    }
  }
}
</script>

<style scoped>
.outs-tracker {
  margin-top: 30px;
  margin-bottom: 30px;
}
.playerCardsHolder {
  margin-bottom: 20px;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 10px;
  background: #f9f9f9;
  box-shadow: 1px 2px 6px #eee;
}
.playerCardsTitle {
  margin-bottom: 10px;
}
.outsDisplay {
  margin-top: 10px;
  font-size: 1.2em;
  color: #0a0a0a;
}
.playingCard {
  display: inline-block;
  margin: 5px;
}
.cardImage {
  height: 60px;
  border-radius: 4px;
  border: 1px solid #aaa;
}
.communityCards {
  margin-top: 20px;
  margin-bottom: 20px;
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
</style>
