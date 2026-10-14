<template>
  <div class="holdem-ai-wrapper">
    <!-- Top Hero Banner -->
    <div class="ai-banner">
      <div class="banner-content">
        <div class="logo-title">
          <span class="poker-suit-symbol">♠</span>
          <div>
            <h1 class="page-title">Texas Hold'em AI Advisor</h1>
            <p class="page-subtitle">
              Deep Reinforcement Learning &amp; Game State Strategy Engine (powered by <code>texas-hold-em-utils</code>)
            </p>
          </div>
        </div>
        <div class="model-status-pill">
          <span class="pulse-indicator"></span>
          <span>GTO Model Active</span>
        </div>
      </div>
    </div>

    <!-- Quick Scenarios Presets -->
    <div class="presets-bar">
      <span class="presets-heading">Quick Scenarios:</span>
      <div class="presets-container">
        <button
          v-for="preset in presets"
          :key="preset.id"
          class="preset-chip-btn"
          @click="loadPreset(preset)"
        >
          {{ preset.name }}
        </button>
      </div>
    </div>

    <!-- Main 2-Column Grid -->
    <div class="dashboard-grid">
      <!-- Left Panel: Scenario Builder -->
      <section class="ai-panel config-panel">
        <div class="panel-top">
          <h2><span class="icon">🎮</span> Scenario Builder</h2>
          <button class="btn-ghost" @click="resetScenario">Reset All</button>
        </div>

        <!-- Hole Cards -->
        <div class="form-section">
          <label class="section-title">Hole Cards (2 Cards)</label>
          <div class="cards-row">
            <div
              v-for="(card, idx) in holeCards"
              :key="'hole-' + idx"
              class="card-slot"
              :class="{ empty: !card, filled: !!card }"
              @click="openPicker('hole', idx)"
            >
              <template v-if="card">
                <div class="card-display">
                  <span class="card-rank" :class="getSuitClass(card)">{{ getCardRank(card) }}</span>
                  <span class="card-suit" :class="getSuitClass(card)">{{ getSuitSymbol(card) }}</span>
                </div>
              </template>
              <template v-else>
                <span class="plus-icon">+</span>
                <span class="slot-label">Card {{ idx + 1 }}</span>
              </template>
            </div>
          </div>
        </div>

        <!-- Community Cards -->
        <div class="form-section">
          <div class="section-header-flex">
            <label class="section-title">Community Cards (Flop, Turn, River)</label>
            <button class="btn-tiny" @click="clearCommunityCards">Clear Board</button>
          </div>
          <div class="cards-row community-row">
            <div
              v-for="(card, idx) in communityCards"
              :key="'comm-' + idx"
              class="card-slot"
              :class="{ empty: !card, filled: !!card }"
              @click="openPicker('comm', idx)"
            >
              <template v-if="card">
                <div class="card-display">
                  <span class="card-rank" :class="getSuitClass(card)">{{ getCardRank(card) }}</span>
                  <span class="card-suit" :class="getSuitClass(card)">{{ getSuitSymbol(card) }}</span>
                </div>
              </template>
              <template v-else>
                <span class="plus-icon">+</span>
                <span class="slot-label">{{ communityStages[idx] }}</span>
              </template>
            </div>
          </div>
        </div>

        <!-- Game Parameters Inputs -->
        <div class="input-grid">
          <div class="input-box">
            <label>Current Pot ($)</label>
            <input type="number" v-model.number="pot" min="1" step="10" />
          </div>
          <div class="input-box">
            <label>Highest Bet / To Call ($)</label>
            <input type="number" v-model.number="allDay" min="0" step="5" />
          </div>
        </div>

        <div class="input-grid">
          <div class="input-box">
            <label>Your Stack Size ($)</label>
            <input type="number" v-model.number="stack" min="1" step="50" />
          </div>
          <div class="input-box">
            <label>Big Blind ($)</label>
            <input type="number" v-model.number="bigBlind" min="1" step="5" />
          </div>
        </div>

        <div class="input-grid">
          <div class="input-box">
            <label>Seat Position</label>
            <select v-model.number="position">
              <option :value="0">Position 0 (Small Blind)</option>
              <option :value="1">Position 1 (Big Blind)</option>
              <option :value="2">Position 2 (Early / UTG)</option>
              <option :value="3">Position 3 (Middle)</option>
              <option :value="4">Position 4 (Cutoff)</option>
              <option :value="5">Position 5 (Button)</option>
            </select>
          </div>
          <div class="input-box">
            <label>Total Players</label>
            <select v-model.number="playerCt">
              <option :value="2">2 Players (Heads Up)</option>
              <option :value="3">3 Players</option>
              <option :value="4">4 Players</option>
              <option :value="6">6 Players (6-Max)</option>
              <option :value="9">9 Players (Full Ring)</option>
            </select>
          </div>
        </div>

        <!-- Analyze Button -->
        <button class="btn-analyze" :disabled="loading" @click="analyzeScenario">
          <span v-if="loading" class="spinner-small"></span>
          <span v-else class="sparkle-icon">✦</span>
          <span>{{ loading ? 'ANALYZING SCENARIO...' : 'ANALYZE SCENARIO & GET MOVE' }}</span>
        </button>

        <div v-if="errorMessage" class="error-banner">
          {{ errorMessage }}
        </div>
      </section>

      <!-- Right Panel: Optimal Strategy Response -->
      <section class="ai-panel results-panel">
        <div class="panel-top">
          <h2><span class="icon">📊</span> Optimal Strategy Response</h2>
          <span class="stage-pill">{{ currentStage }}</span>
        </div>

        <!-- Hero Decision Box -->
        <div class="hero-decision-box" :class="heroActionClass">
          <div class="hero-header">
            <span class="hero-label">RECOMMENDED MOVE</span>
            <span class="ev-chip">EV: {{ formatEV(predictionData?.state_value_estimate) }} BB</span>
          </div>
          <div class="hero-body">
            <h1 class="hero-action-title">{{ formatActionTitle(predictionData?.recommended_action) }}</h1>
            <div
              v-if="predictionData?.action_type !== 'fold' && predictionData?.action_type !== 'check'"
              class="bet-amount-chip"
            >
              <span class="bet-label">Suggested Bet:</span>
              <span class="bet-value">${{ predictionData?.recommended_bet_amount || 0 }} chips</span>
            </div>
          </div>
        </div>

        <!-- Action Probabilities Distribution -->
        <div class="probabilities-section">
          <h3>Action Probability Distribution</h3>
          <div class="probabilities-list">
            <div
              v-for="(prob, actKey) in actionProbabilities"
              :key="actKey"
              class="prob-row"
            >
              <div class="prob-header">
                <span class="prob-name">{{ actionLabels[actKey] || actKey }}</span>
                <span class="prob-percent">{{ (prob * 100).toFixed(1) }}%</span>
              </div>
              <div class="prob-track">
                <div
                  class="prob-bar"
                  :class="{ 'bar-dominant': actKey === predictionData?.recommended_action }"
                  :style="{ width: (prob * 100) + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Statistical Analysis Grid -->
        <div class="statistics-section">
          <h3>Statistical Analysis (via texas_hold_em_utils)</h3>
          <div class="stats-cards-grid">
            <div class="metric-card">
              <span class="metric-title">Expected Win Rate</span>
              <span class="metric-value text-emerald">
                {{ formatPercent(predictionData?.hand_analysis?.expected_win_rate) }}
              </span>
              <span class="metric-caption">Multi-player estimate</span>
            </div>
            <div class="metric-card">
              <span class="metric-title">2-Player Win Rate</span>
              <span class="metric-value">
                {{ formatPercent(predictionData?.hand_analysis?.expected_2_player_win_rate) }}
              </span>
              <span class="metric-caption">Heads-up baseline</span>
            </div>
            <div class="metric-card">
              <span class="metric-title">Percentile Rank</span>
              <span class="metric-value text-gold">
                {{ formatNumber(predictionData?.hand_analysis?.percentile_rank) }}th
              </span>
              <span class="metric-caption">Relative hand strength</span>
            </div>
            <div class="metric-card">
              <span class="metric-title">Sklansky Group</span>
              <span class="metric-value">
                Group {{ predictionData?.hand_analysis?.sklansky_group ?? '-' }}
              </span>
              <span class="metric-caption">Starting hand tier</span>
            </div>
            <div class="metric-card">
              <span class="metric-title">Ideal Kelly Max</span>
              <span class="metric-value">
                {{ formatPercent(predictionData?.hand_analysis?.ideal_kelly_max) }}
              </span>
              <span class="metric-caption">Optimal stack ratio</span>
            </div>
            <div class="metric-card">
              <span class="metric-title">Pot Odds</span>
              <span class="metric-value">
                {{ formatPercent(predictionData?.hand_analysis?.pot_odds) }}
              </span>
              <span class="metric-caption">Required equity to call</span>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 52-Card Selector Modal -->
    <div v-if="pickerOpen" class="card-modal-backdrop" @click.self="closePicker">
      <div class="card-modal-dialog">
        <div class="modal-dialog-header">
          <h3>{{ pickerTitle }}</h3>
          <button class="modal-close-btn" @click="closePicker">✕</button>
        </div>
        <div class="modal-dialog-body">
          <div class="suits-picker-grid">
            <div v-for="suit in suits" :key="suit.code" class="suit-selection-row">
              <div class="suit-badge" :class="suit.class">
                <span>{{ suit.symbol }}</span>
                <span class="suit-name-text">{{ suit.name }}</span>
              </div>
              <div class="ranks-inline-row">
                <button
                  v-for="rank in ranks"
                  :key="rank + suit.code"
                  class="picker-card-btn"
                  :class="[suit.class, { disabled: isCardDisabled(rank + suit.code) }]"
                  :disabled="isCardDisabled(rank + suit.code)"
                  @click="selectCard(rank + suit.code)"
                >
                  <span class="card-btn-rank">{{ rank }}</span>
                  <span class="card-btn-suit">{{ suit.symbol }}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TexasHoldemAI',
  data() {
    return {
      holeCards: ['As', 'Ks'],
      communityCards: ['Qs', 'Js', '2h', null, null],
      communityStages: ['Flop 1', 'Flop 2', 'Flop 3', 'Turn', 'River'],
      pot: 150,
      allDay: 40,
      stack: 1000,
      bigBlind: 20,
      position: 2,
      playerCt: 4,
      loading: false,
      errorMessage: null,
      pickerOpen: false,
      pickerType: 'hole', // 'hole' or 'comm'
      pickerIndex: 0,
      predictionData: null,
      presets: [
        {
          id: 'preflop_aks',
          name: 'Preflop Premium (A♠ K♠ in Cutoff)',
          hole_cards: ['As', 'Ks'],
          community_cards: [],
          pot: 50,
          all_day: 20,
          round_bet: 0,
          stack: 1000,
          position: 4,
          player_ct: 6,
          big_blind: 20
        },
        {
          id: 'flop_flush_draw',
          name: 'Flop Monster Draw (A♠ K♠ on Q♠ J♠ 2♥)',
          hole_cards: ['As', 'Ks'],
          community_cards: ['Qs', 'Js', '2h'],
          pot: 150,
          all_day: 40,
          round_bet: 0,
          stack: 980,
          position: 2,
          player_ct: 4,
          big_blind: 20
        },
        {
          id: 'turn_full_house',
          name: 'Turn Full House (Q♠ Q♦ on Q♥ J♠ J♣ 5♦)',
          hole_cards: ['Qs', 'Qd'],
          community_cards: ['Qh', 'Js', 'Jc', '5d'],
          pot: 350,
          all_day: 80,
          round_bet: 0,
          stack: 900,
          position: 1,
          player_ct: 3,
          big_blind: 20
        },
        {
          id: 'short_stack_tens',
          name: 'Short Stack 10♣ 10♦ Facing Raise',
          hole_cards: ['10c', '10d'],
          community_cards: [],
          pot: 120,
          all_day: 80,
          round_bet: 20,
          stack: 250,
          position: 1,
          player_ct: 6,
          big_blind: 20
        },
        {
          id: 'river_weak_ace',
          name: 'River Weak Ace Facing Large Bet',
          hole_cards: ['Ah', '5h'],
          community_cards: ['Kd', '10s', '8c', '2h', 'Jd'],
          pot: 400,
          all_day: 200,
          round_bet: 0,
          stack: 800,
          position: 0,
          player_ct: 2,
          big_blind: 20
        }
      ],
      ranks: ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2'],
      suits: [
        { code: 's', name: 'Spades', symbol: '♠', class: 'suit-spades' },
        { code: 'h', name: 'Hearts', symbol: '♥', class: 'suit-hearts' },
        { code: 'd', name: 'Diamonds', symbol: '♦', class: 'suit-diamonds' },
        { code: 'c', name: 'Clubs', symbol: '♣', class: 'suit-clubs' }
      ],
      actionLabels: {
        fold: 'Fold',
        check_call: 'Check / Call',
        raise_small: 'Raise Small (Min/0.5x Pot)',
        raise_med: 'Raise Medium (1.0x Pot)',
        raise_allin: 'Raise All-In'
      }
    }
  },
  computed: {
    currentStage() {
      const activeComm = this.communityCards.filter(Boolean).length
      if (activeComm >= 5) return 'RIVER'
      if (activeComm >= 4) return 'TURN'
      if (activeComm >= 3) return 'FLOP'
      return 'PREFLOP'
    },
    heroActionClass() {
      const actionType = this.predictionData?.action_type
      if (actionType === 'raise') return 'action-raise'
      if (actionType === 'call') return 'action-call'
      if (actionType === 'check') return 'action-check'
      return 'action-fold'
    },
    actionProbabilities() {
      return (
        this.predictionData?.action_probabilities || {
          fold: 0.05,
          check_call: 0.2,
          raise_small: 0.55,
          raise_med: 0.15,
          raise_allin: 0.05
        }
      )
    },
    pickerTitle() {
      if (this.pickerType === 'hole') {
        return `Select Hole Card ${this.pickerIndex + 1}`
      }
      return `Select Community Card (${this.communityStages[this.pickerIndex]})`
    }
  },
  mounted() {
    this.fetchPresets()
    this.analyzeScenario()
  },
  methods: {
    getEndpoint() {
      return process.env.VUE_APP_REST_ENDPOINT || ''
    },
    async fetchPresets() {
      try {
        const res = await axios.get(`${this.getEndpoint()}/api/presets`)
        if (res.data && res.data.status === 'success' && res.data.presets) {
          this.presets = res.data.presets
        }
      } catch (err) {
        // Fall back to built-in presets
      }
    },
    loadPreset(preset) {
      this.holeCards = [preset.hole_cards[0] || null, preset.hole_cards[1] || null]
      this.communityCards = [null, null, null, null, null]
      preset.community_cards.forEach((c, idx) => {
        if (idx < 5) this.communityCards[idx] = c
      })
      this.pot = preset.pot
      this.allDay = preset.all_day
      this.stack = preset.stack
      this.position = preset.position
      this.playerCt = preset.player_ct
      this.bigBlind = preset.big_blind

      this.analyzeScenario()
    },
    resetScenario() {
      this.holeCards = [null, null]
      this.communityCards = [null, null, null, null, null]
      this.errorMessage = null
    },
    clearCommunityCards() {
      this.communityCards = [null, null, null, null, null]
    },
    openPicker(type, index) {
      this.pickerType = type
      this.pickerIndex = index
      this.pickerOpen = true
    },
    closePicker() {
      this.pickerOpen = false
    },
    selectCard(cardCode) {
      if (this.pickerType === 'hole') {
        this.holeCards[this.pickerIndex] = cardCode
      } else {
        this.communityCards[this.pickerIndex] = cardCode
      }
      this.closePicker()
    },
    isCardDisabled(cardCode) {
      const currentSelected =
        this.pickerType === 'hole'
          ? this.holeCards[this.pickerIndex]
          : this.communityCards[this.pickerIndex]

      if (cardCode === currentSelected) return false

      const inHole = this.holeCards.filter(Boolean).includes(cardCode)
      const inComm = this.communityCards.filter(Boolean).includes(cardCode)
      return inHole || inComm
    },
    getCardRank(cardCode) {
      if (!cardCode) return ''
      return cardCode.slice(0, -1)
    },
    getSuitSymbol(cardCode) {
      if (!cardCode) return ''
      const code = cardCode.slice(-1).toLowerCase()
      const suit = this.suits.find((s) => s.code === code)
      return suit ? suit.symbol : ''
    },
    getSuitClass(cardCode) {
      if (!cardCode) return ''
      const code = cardCode.slice(-1).toLowerCase()
      const suit = this.suits.find((s) => s.code === code)
      return suit ? suit.class : ''
    },
    formatEV(ev) {
      if (ev === undefined || ev === null) return '+0.00'
      const num = Number(ev)
      return num >= 0 ? `+${num.toFixed(2)}` : num.toFixed(2)
    },
    formatActionTitle(action) {
      if (!action) return 'RAISE SMALL'
      return action.replace('_', ' ').toUpperCase()
    },
    formatPercent(val) {
      if (val === undefined || val === null) return '--%'
      return `${(Number(val) * 100).toFixed(1)}%`
    },
    formatNumber(val) {
      if (val === undefined || val === null) return '--'
      return Number(val).toFixed(1)
    },
    async analyzeScenario() {
      const activeHole = this.holeCards.filter(Boolean)
      if (activeHole.length !== 2) {
        this.errorMessage = 'Please select exactly 2 Hole Cards before analyzing.'
        return
      }

      const activeComm = this.communityCards.filter(Boolean)
      this.errorMessage = null
      this.loading = true

      const payload = {
        hole_cards: activeHole,
        community_cards: activeComm,
        pot: this.pot,
        all_day: this.allDay,
        round_bet: 0,
        stack: this.stack,
        position: this.position,
        player_ct: this.playerCt,
        big_blind: this.bigBlind
      }

      try {
        const res = await axios.post(`${this.getEndpoint()}/api/predict`, payload)
        if (res.data && res.data.status === 'success') {
          this.predictionData = res.data.data
        } else {
          this.errorMessage = res.data?.message || 'Prediction returned an error'
        }
      } catch (err) {
        console.error('Prediction API error:', err)
        // If backend is not running or encountered an issue, provide a helpful message
        this.errorMessage =
          'Could not reach AI backend endpoint (/api/predict). Please ensure the backend server is running.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
/* Main Container & Layout */
.holdem-ai-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 10px 20px 40px;
  text-align: left;
  color: #f3f4f6;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* Banner */
.ai-banner {
  background: linear-gradient(135deg, rgba(17, 24, 39, 0.95) 0%, rgba(31, 41, 55, 0.9) 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 20px 28px;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.banner-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.logo-title {
  display: flex;
  align-items: center;
  gap: 16px;
}

.poker-suit-symbol {
  font-size: 38px;
  color: #f59e0b;
  text-shadow: 0 0 16px rgba(245, 158, 11, 0.6);
}

.page-title {
  font-size: 26px;
  font-weight: 800;
  margin: 0;
  background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.page-subtitle {
  font-size: 13px;
  color: #94a3b8;
  margin: 4px 0 0;
}

.page-subtitle code {
  color: #10b981;
  background: rgba(16, 185, 129, 0.12);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
}

.model-status-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.4);
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  color: #10b981;
  font-weight: 600;
}

.pulse-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #10b981;
  box-shadow: 0 0 10px #10b981;
  animation: pulse-glow 2s infinite;
}

@keyframes pulse-glow {
  0% { transform: scale(0.95); opacity: 0.8; }
  50% { transform: scale(1.2); opacity: 1; }
  100% { transform: scale(0.95); opacity: 0.8; }
}

/* Presets Bar */
.presets-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  overflow-x: auto;
  padding-bottom: 6px;
}

.presets-heading {
  font-size: 13px;
  font-weight: 700;
  color: #94a3b8;
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.presets-container {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.preset-chip-btn {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #cbd5e1;
  padding: 7px 14px;
  border-radius: 20px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.preset-chip-btn:hover {
  background: rgba(99, 102, 241, 0.2);
  border-color: #6366f1;
  color: #fff;
  transform: translateY(-1px);
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

@media (max-width: 992px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

/* Panel Containers */
.ai-panel {
  background: rgba(18, 24, 38, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(12px);
}

.panel-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  padding-bottom: 12px;
}

.panel-top h2 {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
  color: #f1f5f9;
}

.btn-ghost {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 13px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: color 0.2s;
}

.btn-ghost:hover {
  color: #f43f5e;
}

.btn-tiny {
  background: rgba(244, 63, 94, 0.15);
  border: 1px solid rgba(244, 63, 94, 0.3);
  color: #f43f5e;
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-tiny:hover {
  background: rgba(244, 63, 94, 0.3);
}

/* Card Selection Slots */
.form-section {
  margin-bottom: 20px;
}

.section-title {
  display: block;
  font-size: 12px;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.section-header-flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.cards-row {
  display: flex;
  gap: 12px;
}

.community-row {
  flex-wrap: wrap;
}

.card-slot {
  width: 72px;
  height: 98px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  user-select: none;
}

.card-slot.empty {
  background: rgba(15, 23, 42, 0.6);
  border: 2px dashed rgba(255, 255, 255, 0.15);
  color: #64748b;
}

.card-slot.empty:hover {
  border-color: #6366f1;
  background: rgba(99, 102, 241, 0.08);
  transform: translateY(-2px);
}

.card-slot.filled {
  background: linear-gradient(145deg, #ffffff 0%, #f1f5f9 100%);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  transform: translateY(-1px);
}

.card-slot.filled:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}

.plus-icon {
  font-size: 20px;
  line-height: 1;
  margin-bottom: 4px;
}

.slot-label {
  font-size: 11px;
  font-weight: 600;
}

.card-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.card-rank {
  font-size: 22px;
  font-weight: 800;
  line-height: 1.1;
}

.card-suit {
  font-size: 26px;
  line-height: 1;
}

/* Suit Colors */
.suit-spades, .suit-clubs {
  color: #0f172a !important;
}

.suit-hearts, .suit-diamonds {
  color: #dc2626 !important;
}

/* Form Inputs Grid */
.input-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 14px;
}

.input-box {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.input-box label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
}

.input-box input,
.input-box select {
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #f1f5f9;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.input-box input:focus,
.input-box select:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

/* Analyze Button */
.btn-analyze {
  width: 100%;
  margin-top: 10px;
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  border: none;
  color: #fff;
  padding: 14px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
  transition: all 0.2s ease;
}

.btn-analyze:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(99, 102, 241, 0.5);
}

.btn-analyze:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.sparkle-icon {
  font-size: 16px;
  color: #fef08a;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-banner {
  margin-top: 12px;
  padding: 10px 14px;
  background: rgba(244, 63, 94, 0.15);
  border: 1px solid rgba(244, 63, 94, 0.3);
  color: #fca5a5;
  border-radius: 8px;
  font-size: 13px;
}

/* Results Panel Components */
.stage-pill {
  background: rgba(99, 102, 241, 0.15);
  border: 1px solid rgba(99, 102, 241, 0.3);
  color: #a5b4fc;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
}

/* Hero Decision Box */
.hero-decision-box {
  border-radius: 14px;
  padding: 20px;
  margin-bottom: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.hero-decision-box.action-raise {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.18) 0%, rgba(147, 51, 234, 0.12) 100%);
  border-color: rgba(99, 102, 241, 0.4);
  box-shadow: 0 0 25px rgba(99, 102, 241, 0.2);
}

.hero-decision-box.action-call {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.18) 0%, rgba(5, 150, 105, 0.12) 100%);
  border-color: rgba(16, 185, 129, 0.4);
  box-shadow: 0 0 25px rgba(16, 185, 129, 0.2);
}

.hero-decision-box.action-check {
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.18) 0%, rgba(14, 116, 144, 0.12) 100%);
  border-color: rgba(6, 182, 212, 0.4);
  box-shadow: 0 0 25px rgba(6, 182, 212, 0.2);
}

.hero-decision-box.action-fold {
  background: linear-gradient(135deg, rgba(244, 63, 94, 0.18) 0%, rgba(190, 18, 60, 0.12) 100%);
  border-color: rgba(244, 63, 94, 0.4);
  box-shadow: 0 0 25px rgba(244, 63, 94, 0.2);
}

.hero-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.hero-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #94a3b8;
}

.ev-chip {
  font-size: 12px;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.1);
  padding: 3px 8px;
  border-radius: 6px;
  color: #38bdf8;
}

.hero-body {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.hero-action-title {
  font-size: 28px;
  font-weight: 900;
  letter-spacing: 0.5px;
  margin: 0;
  color: #fff;
}

.bet-amount-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(0, 0, 0, 0.3);
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.bet-label {
  font-size: 12px;
  color: #94a3b8;
}

.bet-value {
  font-size: 14px;
  font-weight: 700;
  color: #fbbf24;
}

/* Probabilities Section */
.probabilities-section {
  margin-bottom: 24px;
}

.probabilities-section h3,
.statistics-section h3 {
  font-size: 14px;
  font-weight: 700;
  color: #cbd5e1;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.probabilities-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.prob-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.prob-header {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #cbd5e1;
}

.prob-percent {
  font-weight: 700;
  color: #f1f5f9;
}

.prob-track {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  overflow: hidden;
}

.prob-bar {
  height: 100%;
  background: #64748b;
  border-radius: 4px;
  transition: width 0.4s ease;
}

.prob-bar.bar-dominant {
  background: linear-gradient(90deg, #6366f1 0%, #10b981 100%);
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
}

/* Statistics Grid */
.stats-cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

@media (max-width: 600px) {
  .stats-cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.metric-card {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.metric-title {
  font-size: 11px;
  color: #94a3b8;
  font-weight: 600;
}

.metric-value {
  font-size: 18px;
  font-weight: 800;
  color: #f1f5f9;
}

.metric-caption {
  font-size: 10px;
  color: #64748b;
}

.text-emerald {
  color: #10b981 !important;
}

.text-gold {
  color: #f59e0b !important;
}

/* Card Picker Modal */
.card-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 16px;
}

.card-modal-dialog {
  background: #0f172a;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  max-width: 820px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
}

.modal-dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.modal-dialog-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #fff;
}

.modal-close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 20px;
  cursor: pointer;
  padding: 4px;
  line-height: 1;
}

.modal-close-btn:hover {
  color: #fff;
}

.modal-dialog-body {
  padding: 20px 24px 28px;
}

.suits-picker-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.suit-selection-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.suit-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  width: 90px;
  font-size: 16px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.05);
}

.suit-name-text {
  font-size: 13px;
}

.ranks-inline-row {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  flex: 1;
}

.picker-card-btn {
  width: 44px;
  height: 56px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
  padding: 2px;
}

.picker-card-btn:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  border-color: #6366f1;
}

.picker-card-btn.disabled {
  opacity: 0.25;
  cursor: not-allowed;
  filter: grayscale(1);
}

.card-btn-rank {
  font-size: 15px;
  font-weight: 800;
  line-height: 1;
}

.card-btn-suit {
  font-size: 18px;
  line-height: 1;
}
</style>
