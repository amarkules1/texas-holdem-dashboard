<template>
    <div class="container mt-5">
        <div class="row mb-4">
            <div class="col text-center text-white">
                <h1>Welcome to CasinoSolver</h1>
                <p class="lead">Select a tool to get started</p>
            </div>
        </div>
        <div class="row justify-content-center">
            <div class="col-md-4 mb-4" v-for="tool in tools" :key="tool.path">
                <div class="card h-100 bg-dark text-white border-secondary tool-card" @click="$router.push(tool.path)">
                    <div class="card-body text-center">
                        <h5 class="card-title text-info">{{ tool.title }}</h5>
                        <p class="card-text">{{ tool.description }}</p>
                        <router-link :to="tool.path" class="btn btn-outline-info">Go to Tool</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'HomePage',
    data() {
        return {
            tools: [
                {
                    title: "Poker Hand Stats",
                    description: "Analyze your Texas Hold'em hand strength, win rates, and determine the best move for specific scenarios.",
                    path: "/poker-hand-stats"
                },
                {
                    title: "Hand Comparison",
                    description: "Compare poker hands to see their odds of beating eachother, watch the odds change through the flop, turn, and river.",
                    path: "/hand-comparison"
                },
                {
                    title: "Outs Tracker",
                    description: "See each player's outs in a game based on all known cards.",
                    path: "/outs-tracker"
                },
                {
                    title: "Bet Analysis",
                    description: "Analyze betting odds to find the implied probability of each outcome and determine the house edge. Also works for finding arbitrage opportunities.",
                    path: "/bet-analysis"
                },
                {
                    title: "Blackjack Strategy",
                    description: "Blackjack basic strategy charts for a variety of game rule sets.",
                    path: "/blackjack-strategy"
                },
                {
                    title: "Blackjack Quiz",
                    description: "Test your Blackjack basic strategy knowledge with a quiz.",
                    path: "/blackjack-quiz"
                }
            ]
        }
    }
}
</script>

<style scoped>
.tool-card {
    cursor: pointer;
    transition: transform 0.2s;
}

.tool-card:hover {
    transform: translateY(-5px);
    border-color: #17a2b8 !important;
    /* Bootstrap info color */
}
</style>
