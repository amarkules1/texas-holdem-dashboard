<template>
    <div class="container main-container">
        <h2 class="page-title">Betting Summary Analysis</h2>
        
        <div class="card input-card">
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        <label for="odds1" class="form-label">Odds 1 (American)</label>
                        <input type="number" id="odds1" v-model.number="odds1" class="form-control" placeholder="e.g. -110 or 250">
                    </div>
                    <div class="col-md-4">
                        <label for="odds2" class="form-label">Odds 2 (American)</label>
                        <input type="number" id="odds2" v-model.number="odds2" class="form-control" placeholder="e.g. -110 or 250">
                    </div>
                    <div class="col-md-4">
                        <label for="totalBet" class="form-label">Total Bet Amount</label>
                        <input type="number" id="totalBet" v-model.number="totalBet" class="form-control" placeholder="100">
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-12 text-center">
                        <button @click="calculateBetSummary" class="btn btn-primary calculate-btn" :disabled="loading">
                            <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                            Calculate
                        </button>
                    </div>
                </div>
                <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
            </div>
        </div>

        <div v-if="results" class="card result-card mt-4">
            <div class="card-header">Results</div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6 result-column">
                        <h4>Outcome 1</h4>
                        <p><strong>Probability:</strong> {{ (results.percent_probability * 100).toFixed(2) }}%</p>
                        <p><strong>Bet Amount:</strong> ${{ results.bet_amount.toFixed(2) }}</p>
                    </div>
                    <div class="col-md-6 result-column">
                        <h4>Outcome 2</h4>
                        <p><strong>Probability:</strong> {{ (results.opp_percent_probability * 100).toFixed(2) }}%</p>
                        <p><strong>Bet Amount:</strong> ${{ results.bet_amount_opp.toFixed(2) }}</p>
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-12 text-center">
                        <h3>Expected Return: ${{ results.expected_return.toFixed(2) }}</h3>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'BetSummary',
    data() {
        return {
            odds1: null,
            odds2: null,
            totalBet: 100,
            results: null,
            loading: false,
            error: null
        }
    },
    methods: {
        async calculateBetSummary() {
            if (this.odds1 === null || this.odds2 === null) {
                this.error = "Please enter both odds."
                return
            }
            this.error = null
            this.loading = true
            this.results = null
            
            try {
                let endpoint = process.env.VUE_APP_REST_ENDPOINT || 'http://localhost:5000'
                // Remove trailing slash if present
                if (endpoint.endsWith('/')) {
                    endpoint = endpoint.slice(0, -1) 
                }
                
                const response = await axios.get(`${endpoint}/bet-summary`, {
                    params: {
                        odds_1: this.odds1,
                        odds_2: this.odds2,
                        total_bet: this.totalBet
                    }
                })
                this.results = response.data
            } catch (err) {
                console.error(err)
                this.error = "Failed to fetch bet summary. Please try again."
            } finally {
                this.loading = false
            }
        }
    }
}
</script>

<style scoped>
.main-container {
    padding-top: 20px;
    color: #333;
}
.page-title {
    color: #fff;
    margin-bottom: 20px;
}
.input-card, .result-card {
    background-color: #f8f9fa;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.calculate-btn {
    width: 200px;
    font-size: 1.1em;
}
.result-column {
    border-right: 1px solid #dee2e6;
}
.result-column:last-child {
    border-right: none;
}
h4 {
    color: #0d6efd;
}
</style>
