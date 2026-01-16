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
                    description: "Analyze your Texas Hold'em hand strength, win rates, and get betting advice based on the Kelly Criterion.",
                    path: "/poker-hand-stats"
                },
                {
                    title: "Hand Comparison",
                    description: "Compare two specific poker hands to see which one wins.",
                    path: "/hand-comparison"
                },
                {
                    title: "Outs Tracker",
                    description: "Track your outs in a live game.",
                    path: "/outs-tracker"
                },
                {
                    title: "Bet Analysis",
                    description: "Analyze your betting history (requires uploaded data).",
                    path: "/bet-analysis"
                },
                {
                    title: "Blackjack Strategy",
                    description: "Learn optimal Blackjack strategy.",
                    path: "/blackjack-strategy"
                },
                {
                    title: "Blackjack Quiz",
                    description: "Test your Blackjack skills with a quiz.",
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
