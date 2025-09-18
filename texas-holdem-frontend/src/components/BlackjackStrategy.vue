<template>
  <div>
    <h2>Blackjack Basic Strategy</h2>
    <div class="controls">
      <label>
        <input type="checkbox" v-model="dealerHitSoft17" />
        Dealer hits on soft 17
      </label>
      <label>
        <input type="checkbox" v-model="doubleAfterSplit" />
        Double after split allowed
      </label>
      <label>
        Blackjack pays:
        <input type="number" v-model.number="blackjackPays" step="0.1" />
      </label>
      <button @click="fetchStrategy">Get Strategy</button>
    </div>
    <table v-if="strategyData.length" class="strategy-table">
      <thead>
        <tr>
          <th>Player Total</th>
          <th v-for="dealerCard in dealerCards" :key="dealerCard">{{ dealerCard }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="playerTotal in playerTotals" :key="playerTotal">
          <td>{{ playerTotal }}</td>
          <td v-for="dealerCard in dealerCards" :key="dealerCard">
            {{ getAction(playerTotal, dealerCard) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BlackjackStrategy',
  data() {
    return {
      dealerHitSoft17: true,
      doubleAfterSplit: true,
      blackjackPays: 1.5,
      strategyData: [],
    };
  },
  computed: {
    playerTotals() {
      return [...new Set(this.strategyData.map(item => item.player_total))].sort((a, b) => a - b);
    },
    dealerCards() {
      return [...new Set(this.strategyData.map(item => item.dealer_card_up))].sort((a, b) => a - b);
    },
  },
  methods: {
    async fetchStrategy() {
      try {
        const params = {
          dealer_hit_soft_17: this.dealerHitSoft17,
          double_after_split: this.doubleAfterSplit,
          blackjack_pays: this.blackjackPays,
        };
        const response = await axios.get('http://localhost:5000/blackjack-basic-strategy', { params });
        this.strategyData = response.data;
      } catch (error) {
        console.error('Error fetching blackjack strategy:', error);
      }
    },
    getAction(playerTotal, dealerCard) {
      const entry = this.strategyData.find(
        item => item.player_total === playerTotal && item.dealer_card_up === dealerCard
      );
      return entry ? entry.best_action : '';
    },
  },
  mounted() {
    this.fetchStrategy();
  },
};
</script>

<style scoped>
.controls {
  margin-bottom: 20px;
}
.controls label {
  margin-right: 15px;
}
.strategy-table {
  width: 100%;
  border-collapse: collapse;
}
.strategy-table th,
.strategy-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
.strategy-table th {
  background-color: #f2f2f2;
}
</style>
