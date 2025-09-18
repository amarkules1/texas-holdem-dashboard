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
        <select v-model.number="blackjackPays">
          <option value="1.5">3:2</option>
          <option value="1.2">6:5</option>
        </select>
      </label>
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
          <td>{{ formatPlayerTotal(playerTotal) }}</td>
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
  watch: {
    dealerHitSoft17() {
      this.fetchStrategy();
    },
    doubleAfterSplit() {
      this.fetchStrategy();
    },
    blackjackPays() {
      this.fetchStrategy();
    },
  },
  computed: {
    playerTotals() {
      const totals = [...new Set(this.strategyData.map(item => item.player_total))];
      return totals.sort((a, b) => {
        const aIsNum = !isNaN(a);
        const bIsNum = !isNaN(b);

        if (aIsNum && bIsNum) {
          return a - b; // Sort numbers numerically
        }
        if (aIsNum && !bIsNum) {
          return -1; // Numbers come before strings
        }
        if (!aIsNum && bIsNum) {
          return 1; // Strings come after numbers
        }
        // Both are strings, sort alphabetically
        return a.localeCompare(b);
      });
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
    formatPlayerTotal(total) {
      if (typeof total === 'string') {
        return total
          .split('_')
          .map(word => word.charAt(0).toUpperCase() + word.slice(1))
          .join(' ');
      }
      return total;
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
  background-color: #6c757d; /* A darker gray from Bootstrap's color palette */
  color: white;
}
</style>
