<template>
    <div >
        <div class="buttonsContainer container">
            <div class="row">
                <div class="col-6">
                    <label for="search" v-if="!(selectedPlayerStats && selectedPlayerStats.length)">Search: &nbsp;</label>
                    <input class="searchBar" v-model="search" placeholder="Search by username" @keyup="searchPlayers" v-if="!(selectedPlayerStats && selectedPlayerStats.length)"/>
                </div>
                <div class="col-6">
                    <label for="gameFile">Upload Game File: &nbsp;</label>
                    <input type="file" @change="handleFileUpload" ref="fileInput"/>
                </div>
            </div>
        </div>
        <div class="tableContainer" v-if="selectedPlayerStats && selectedPlayerStats.length">
            <DataTable :value="selectedPlayerStats" tableStyle="min-width: 50rem">
                <Column header="Remove">
                    <template #body="slotProps">
                        <button @click="removePlayer(slotProps.data.username)" class="btn btn-danger">Remove</button>
                    </template>
                </Column>
                <Column v-for="col of columns" sortable :key="col.field" :field="col.field" :header="col.header"></Column>
            </DataTable>
        </div>
        <div class="buttonsContainer container" v-if="selectedPlayerStats && selectedPlayerStats.length">
            <div class="row">
                <div class="col-6" v-if="selectedPlayerStats && selectedPlayerStats.length">
                    <label for="search">Search: &nbsp;</label>
                    <input class="searchBar" v-model="search" placeholder="Search by username" @keyup="searchPlayers"/>
                </div>
            </div>
        </div>
        <div class="tableContainer" v-if="playerStats && playerStats.length">
            <DataTable :value="playerStats" tableStyle="min-width: 50rem">
                <Column header="Add">
                    <template #body="slotProps">
                        <button @click="addPlayer(slotProps.data.username)" class="btn btn-success">Add</button>
                    </template>
                </Column>
                <Column v-for="col of columns" sortable :key="col.field" :field="col.field" :header="col.header"></Column>
            </DataTable>
        </div>
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
            allPlayerStats: null,
            selectedPlayers: [],
            selectedPlayerStats: [],
            search: null,
            gameFile: null,
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
    async beforeMount() {
        this.playerStats = await this.getPlayerStats()
        this.allPlayerStats = this.playerStats
    },
    methods: {
        async getPlayerStats() {
            const response = await axios.get(process.env.VUE_APP_REST_ENDPOINT + "/player-summaries")
            return response.data
        },
        searchPlayers() {
            this.playerStats = this.allPlayerStats.filter(player => player.username.toLowerCase().includes(this.search.toLowerCase()))
        },
        handleFileUpload() {
            this.gameFile = this.$refs.fileInput.files[0]
            const formData = new FormData()
            formData.append('file', this.gameFile)
            axios.post(process.env.VUE_APP_REST_ENDPOINT + "/game-file", formData)
        },
        addPlayer(username) {
            this.selectedPlayers.push(username)
            this.selectedPlayerStats = this.allPlayerStats.filter(player => this.selectedPlayers.includes(player.username))
        },
        removePlayer(username) {
            this.selectedPlayers = this.selectedPlayers.filter(player => player !== username)
            this.selectedPlayerStats = this.allPlayerStats.filter(player => this.selectedPlayers.includes(player.username))
        }
    }
}
</script>

<style scoped>
.tableContainer {
    margin-top: 40px;
    margin-bottom: 60px;
    width: 90%;
    margin-right: auto;
    margin-left: auto;
}
</style>