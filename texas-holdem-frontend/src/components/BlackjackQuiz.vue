<template>
  <div class="blackjack-quiz">
    <h2>Blackjack Strategy Quiz</h2>
    
    <!-- Game Settings -->
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

    <!-- Quiz Section -->
    <div v-if="currentScenario" class="quiz-container">
      <div class="scenario">
        <h3>Scenario {{ currentQuestionNumber }}</h3>
        
        <!-- Cards Display -->
        <div class="cards-display">
          <div class="dealer-section">
            <h4>Dealer's Up Card</h4>
            <div class="card dealer-card">{{ currentScenario.dealer_card_up }}</div>
          </div>
          
          <div class="player-section">
            <h4>Your Hand: {{ formatPlayerTotal(currentScenario.player_total) }}</h4>
            <div class="player-cards">
              <div class="card player-card" v-for="(card, index) in getPlayerCards(currentScenario.player_total)" :key="index">
                {{ card }}
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div v-if="!showResult" class="action-buttons">
          <h4>What should you do?</h4>
          <button 
            v-for="action in availableActions" 
            :key="action"
            @click="selectAction(action)"
            class="action-btn"
            :class="action.toLowerCase()"
          >
            {{ action }}
          </button>
        </div>

        <!-- Result Display -->
        <div v-if="showResult" class="result-section">
          <div class="result" :class="{ correct: isCorrect, incorrect: !isCorrect }">
            <h4>{{ isCorrect ? '✓ Correct!' : '✗ Incorrect' }}</h4>
            <p>
              <strong>Your answer:</strong> {{ selectedAction }}<br>
              <strong>Correct answer:</strong> {{ correctAction }}
            </p>
            <div v-if="!isCorrect" class="explanation">
              <p><strong>Expected Values:</strong></p>
              <div class="ev-breakdown">
                <div v-if="currentScenario.hit_ev !== null">Hit: {{ currentScenario.hit_ev.toFixed(4) }}</div>
                <div v-if="currentScenario.stand_ev !== null">Stand: {{ currentScenario.stand_ev.toFixed(4) }}</div>
                <div v-if="currentScenario.double_ev !== null">Double: {{ currentScenario.double_ev.toFixed(4) }}</div>
                <div v-if="currentScenario.split_ev !== null">Split: {{ currentScenario.split_ev.toFixed(4) }}</div>
              </div>
            </div>
          </div>
          
          <div class="quiz-controls">
            <button @click="nextQuestion" class="next-btn">Next Question</button>
            <button @click="resetQuiz" class="reset-btn">Reset Quiz</button>
          </div>
        </div>
      </div>

      <!-- Score Display -->
      <div class="score-display">
        <p>Score: {{ correctAnswers }} / {{ totalQuestions }} ({{ scorePercentage }}%)</p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else-if="loading" class="loading">
      Loading quiz scenarios...
    </div>

    <!-- Start Quiz Button -->
    <div v-else class="start-section">
      <button @click="startQuiz" class="start-btn">Start Quiz</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BlackjackQuiz',
  data() {
    return {
      // Game settings (same as BlackjackStrategy component)
      dealerHitSoft17: true,
      doubleAfterSplit: true,
      blackjackPays: 1.5,
      
      // Quiz data
      strategyData: [],
      quizScenarios: [],
      currentScenarioIndex: 0,
      currentQuestionNumber: 1,
      
      // Quiz state
      loading: false,
      showResult: false,
      selectedAction: '',
      correctAnswers: 0,
      totalQuestions: 0,
      
      // Available actions for quiz
      allActions: ['Hit', 'Stand', 'Double', 'Split']
    };
  },
  computed: {
    currentScenario() {
      return this.quizScenarios[this.currentScenarioIndex] || null;
    },
    correctAction() {
      return this.currentScenario ? this.currentScenario.best_action : '';
    },
    isCorrect() {
      return this.selectedAction.toLowerCase() === this.correctAction.toLowerCase();
    },
    scorePercentage() {
      return this.totalQuestions > 0 ? Math.round((this.correctAnswers / this.totalQuestions) * 100) : 0;
    },
    availableActions() {
      if (!this.currentScenario) return [];
      
      const actions = ['Hit', 'Stand'];
      
      // Add Double if available
      if (this.currentScenario.double_ev !== null) {
        actions.push('Double');
      }
      
      // Add Split if available
      if (this.currentScenario.split_ev !== null) {
        actions.push('Split');
      }
      
      return actions;
    }
  },
  watch: {
    dealerHitSoft17() {
      if (this.quizScenarios.length > 0) {
        this.resetQuiz();
      }
    },
    doubleAfterSplit() {
      if (this.quizScenarios.length > 0) {
        this.resetQuiz();
      }
    },
    blackjackPays() {
      if (this.quizScenarios.length > 0) {
        this.resetQuiz();
      }
    }
  },
  methods: {
    async fetchStrategy() {
      try {
        this.loading = true;
        const params = {
          dealer_hit_soft_17: this.dealerHitSoft17,
          double_after_split: this.doubleAfterSplit,
          blackjack_pays: this.blackjackPays,
        };
        const response = await axios.get('http://localhost:5000/blackjack-basic-strategy', { params });
        this.strategyData = response.data;
        this.generateQuizScenarios();
      } catch (error) {
        console.error('Error fetching blackjack strategy:', error);
      } finally {
        this.loading = false;
      }
    },
    
    generateQuizScenarios() {
      // Create a randomized subset of scenarios for the quiz
      const shuffled = [...this.strategyData].sort(() => 0.5 - Math.random());
      this.quizScenarios = shuffled.slice(0, 20); // Take 20 random scenarios
    },
    
    startQuiz() {
      this.fetchStrategy();
    },
    
    resetQuiz() {
      this.currentScenarioIndex = 0;
      this.currentQuestionNumber = 1;
      this.showResult = false;
      this.selectedAction = '';
      this.correctAnswers = 0;
      this.totalQuestions = 0;
      this.fetchStrategy();
    },
    
    selectAction(action) {
      this.selectedAction = action;
      this.totalQuestions++;
      
      if (this.isCorrect) {
        this.correctAnswers++;
      }
      
      this.showResult = true;
    },
    
    nextQuestion() {
      this.currentScenarioIndex++;
      this.currentQuestionNumber++;
      this.showResult = false;
      this.selectedAction = '';
      
      // If we've gone through all scenarios, generate new ones
      if (this.currentScenarioIndex >= this.quizScenarios.length) {
        this.generateQuizScenarios();
        this.currentScenarioIndex = 0;
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
    
    getPlayerCards(playerTotal) {
      // Generate representative cards for display
      if (typeof playerTotal === 'string') {
        if (playerTotal.includes('pair')) {
          const card = playerTotal.replace('pair_', '').toUpperCase();
          return [card, card];
        } else if (playerTotal.includes('soft')) {
          const value = parseInt(playerTotal.replace('soft_', ''));
          const otherCard = value - 11;
          return ['A', otherCard.toString()];
        }
      }
      
      // For hard totals, show representative cards
      const total = parseInt(playerTotal);
      if (total <= 11) {
        return [total.toString()];
      } else if (total <= 21) {
        // Show a reasonable split (e.g., 10+6 for 16)
        const firstCard = Math.min(10, Math.floor(total / 2) + 1);
        const secondCard = total - firstCard;
        return [firstCard.toString(), secondCard.toString()];
      }
      
      return [playerTotal.toString()];
    }
  }
};
</script>

<style scoped>
.blackjack-quiz {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.controls {
  margin-bottom: 30px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  color: #333;
}

.controls label {
  margin-right: 20px;
  display: inline-block;
  margin-bottom: 10px;
}

.quiz-container {
  background-color: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.scenario h3 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.cards-display {
  display: flex;
  justify-content: space-around;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.dealer-section, .player-section {
  text-align: center;
  margin: 20px;
}

.dealer-section h4, .player-section h4 {
  margin-bottom: 15px;
  color: #555;
}

.card {
  display: inline-block;
  width: 60px;
  height: 80px;
  border: 2px solid #333;
  border-radius: 8px;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  margin: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dealer-card {
  background-color: #ffebee;
  color: #c62828;
}

.player-card {
  background-color: #e8f5e8;
  color: #2e7d32;
}

.player-cards {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.action-buttons {
  text-align: center;
  margin-bottom: 30px;
}

.action-buttons h4 {
  margin-bottom: 20px;
  color: #333;
}

.action-btn {
  margin: 10px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 100px;
}

.action-btn.hit {
  background-color: #2196F3;
  color: white;
}

.action-btn.stand {
  background-color: #f44336;
  color: white;
}

.action-btn.double {
  background-color: #4CAF50;
  color: white;
}

.action-btn.split {
  background-color: #FF9800;
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.result-section {
  text-align: center;
}

.result {
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.result.correct {
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  color: #155724;
}

.result.incorrect {
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

.explanation {
  margin-top: 15px;
  text-align: left;
}

.ev-breakdown {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 10px;
  border-radius: 4px;
  margin-top: 10px;
}

.ev-breakdown div {
  margin: 5px 0;
  font-family: monospace;
}

.quiz-controls {
  margin-top: 20px;
}

.next-btn, .reset-btn, .start-btn {
  margin: 10px;
  padding: 12px 24px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}

.next-btn {
  background-color: #007bff;
  color: white;
}

.reset-btn {
  background-color: #6c757d;
  color: white;
}

.start-btn {
  background-color: #28a745;
  color: white;
  font-size: 18px;
  padding: 15px 30px;
}

.next-btn:hover, .reset-btn:hover, .start-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.score-display {
  text-align: center;
  margin-top: 20px;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.loading, .start-section {
  text-align: center;
  padding: 40px;
}

.loading {
  font-size: 18px;
  color: #666;
}
</style>
