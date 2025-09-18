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
          <th></th>
          <th :colspan="dealerCards.length" style="text-align: center;">Dealer's Up Card</th>
        </tr>
        <tr>
          <th>Player Total</th>
          <th v-for="dealerCard in dealerCards" :key="dealerCard">{{ dealerCard }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="playerTotal in playerTotals" :key="playerTotal">
          <td>{{ formatPlayerTotal(playerTotal) }}</td>
          <td 
            v-for="dealerCard in dealerCards" 
            :key="dealerCard" 
            :style="{ backgroundColor: getColorForAction(getAction(playerTotal, dealerCard)) }"
            @mouseenter="(event) => showTooltip(event, playerTotal, dealerCard)"
            @mouseleave="hideTooltip"
          >
            {{ getAction(playerTotal, dealerCard) }}
          </td>
        </tr>
      </tbody>
    </table>
    <Teleport to="body">
      <div v-if="tooltip.visible" class="tooltip" :style="tooltip.style">
        <div v-for="(value, key) in tooltip.content" :key="key">
          <strong>{{ key }}:</strong> {{ value.toFixed(4) }}
        </div>
      </div>
    </Teleport>
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
      tooltip: {
        visible: false,
        content: {},
        style: {},
        timer: null,
      },
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
    getColorForAction(action) {
      if (!action) return '';
      const actionType = action.split('/')[0].toLowerCase(); // Handle cases like 'Double/Hit'
      switch (actionType) {
        case 'stand':
          return 'rgba(255, 87, 87, 0.2)'; // Red
        case 'split':
          return 'rgba(255, 255, 87, 0.2)'; // Yellow
        case 'hit':
          return 'rgba(87, 151, 255, 0.2)'; // Blue
        case 'double':
          return 'rgba(87, 255, 87, 0.2)'; // Green
        default:
          return '';
      }
    },
    showTooltip(event, playerTotal, dealerCard) {
      if (this.tooltip.timer) {
        clearTimeout(this.tooltip.timer);
      }
      this.tooltip.timer = setTimeout(() => {
        const entry = this.strategyData.find(
          item => item.player_total === playerTotal && item.dealer_card_up === dealerCard
        );
        if (!entry) return;

        const content = {};
        if (entry.double_ev !== null) content['Double'] = entry.double_ev;
        if (entry.hit_ev !== null) content['Hit'] = entry.hit_ev;
        if (entry.stand_ev !== null) content['Stand'] = entry.stand_ev;
        if (entry.split_ev !== null) content['Split'] = entry.split_ev;

        if (Object.keys(content).length > 0) {
          const rect = event.target.getBoundingClientRect();
          this.tooltip.content = content;
          this.tooltip.style = {
            left: `${rect.left + rect.width / 2}px`,
            top: `${rect.top - 10}px`,
            transform: 'translateX(-50%) translateY(-100%)',
          };
          this.tooltip.visible = true;
          console.log(playerTotal, dealerCard);
        }
      }, 500);
    },
    hideTooltip() {
      clearTimeout(this.tooltip.timer);
      this.tooltip.visible = false;
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
  max-width: 90%;
  margin: 0 auto;
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
.strategy-table tbody tr td:first-child {
  font-weight: bold;
  background-color: #6c757d;
  color: white;
}
.tooltip {
  position: fixed;
  background-color: #333;
  color: white;
  padding: 10px;
  border-radius: 5px;
  z-index: 1000;
  pointer-events: none; /* Allows mouse events to pass through to elements below */
  font-size: 0.9em;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}
</style>
