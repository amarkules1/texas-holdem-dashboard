<template>
    <div v-if="playerStats">
        <DataTable :value="playerStats" tableStyle="min-width: 50rem">
            <Column v-for="col of columns" :key="col.field" :field="col.field" :header="col.header"></Column>
        </DataTable>
    </div>
</template>
<script>
import axios from 'axios'
import {DataTable} from 'primevue';
import {Column} from 'primevue';
export default {
    name: 'PlayerStats',
    components: {
        DataTable,
        Column
    },
    data() {
        return {
            playerStats: null,
            columns: [
                {field: "username", header: "Username"},
                {field: "profit_loss_per_game", header: "P/L per Game"},
                {field: "game_count", header: "Game Count"},
                {field: "call_rate", header: "Call Rate"},
                {field: "raise_rate", header: "Raise Rate"},
                {field: "preflop_fold_rate", header: "Pre-Flop Fold Rate"},
                {field: "preturn_fold_rate", header: "Pre-Turn Fold Rate"},
                {field: "preriver_fold_rate", header: "Pre-River Fold Rate"},
                {field: "preshowdown_fold_rate", header: "Pre-Showdown Fold Rate"}
            ]
        }
    },
    async mounted() {
        this.playerStats = await this.getPlayerStats()
    },
    methods: {
        async getPlayerStats() {
            const response = await axios.get(process.env.VUE_APP_REST_ENDPOINT + "/player-summaries")
            return response.data
        }
    }
}
</script>

<style scoped>
.statsContainer {
    margin-top: 20px;
    margin-bottom: 20px;
    min-height: 88px;
}

.statsDisplay {
    display: flex;
    justify-content: center;
}
</style>