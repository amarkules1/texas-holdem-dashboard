<template>
    <div class="container main-container">
        <h2 class="page-title">Betting Summary Analysis</h2>
        
        <div class="card input-card">
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3 mb-3" v-for="(odd, index) in oddsList" :key="index">
                        <label :for="'odds' + (index + 1)" class="form-label">Odds {{ index + 1 }} (American)</label>
                        <div class="input-group">
                            <input type="number" :id="'odds' + (index + 1)" v-model.number="oddsList[index]" class="form-control" placeholder="-110">
                            <button v-if="oddsList.length > 2" class="btn btn-outline-danger" type="button" @click="removeOdd(index)" title="Remove odds">-</button>
                        </div>
                    </div>
                    <div class="col-md-3 mb-3 d-flex align-items-end">
                        <button class="btn btn-outline-secondary me-2" type="button" @click="addOdd" title="Add another odds">Add Odds</button>
                    </div>
                    <div class="col-md-12 mt-2">
                        <label for="totalBet" class="form-label">Total Bet Amount</label>
                        <input type="number" id="totalBet" v-model.number="totalBet" class="form-control" style="max-width: 200px;" placeholder="100">
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
                    <div class="col-md-3 result-column mb-3">
                        <h4>Outcome 1</h4>
                        <p><strong>Probability:</strong> {{ (results.percent_probability * 100).toFixed(2) }}%</p>
                        <p><strong>Bet Amount:</strong> ${{ results.bet_amount.toFixed(2) }}</p>
                    </div>
                    <div class="col-md-3 result-column mb-3" v-for="(prob, index) in results.opp_percent_probabilities" :key="index">
                        <h4>Outcome {{ index + 2 }}</h4>
                        <p><strong>Probability:</strong> {{ (prob * 100).toFixed(2) }}%</p>
                        <p><strong>Bet Amount:</strong> ${{ results.other_bets[index].toFixed(2) }}</p>
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
            oddsList: [null, null],
            totalBet: 100,
            results: null,
            loading: false,
            error: null
        }
    },
    methods: {
        addOdd() {
            this.oddsList.push(null);
        },
        removeOdd(index) {
            this.oddsList.splice(index, 1);
        },
        async calculateBetSummary() {
            if (this.oddsList.some(odd => odd === null || odd === '')) {
                this.error = "Please enter all odds."
                return
            }
            this.error = null
            this.loading = true
            this.results = null
            
            try {
                let endpoint = process.env.VUE_APP_REST_ENDPOINT
                
                let params = { total_bet: this.totalBet };
                this.oddsList.forEach((odd, index) => {
                    params[`odds_${index + 1}`] = odd;
                });
                
                const response = await axios.get(`${endpoint}/bet-summary-multi-way`, {
                    params: params
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
