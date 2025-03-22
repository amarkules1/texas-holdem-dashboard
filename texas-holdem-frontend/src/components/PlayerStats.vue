<template>
    <div>
        <div class="buttonsContainer container">
            <div class="row">
                <div class="col-5">
                    <label for="search" v-if="!(selectedPlayerStats && selectedPlayerStats.length)">Search:
                        &nbsp;</label>
                    <input class="searchBar" v-model="search" placeholder="Search by username" @keyup="searchPlayers"
                        v-if="!(selectedPlayerStats && selectedPlayerStats.length)" />
                </div>
                <div class="col-5" v-if="!loadingFile">
                    <label for="gameFile">Upload Game File: &nbsp;</label>
                    <input type="file" @change="handleFileUpload" ref="fileInput" />
                    <p v-if="mostRecentFileName">Successfully uploaded file: {{ mostRecentFileName }}"</p>
                </div>
                <div class="col-5" v-else>
                    <label for="gameFile">Loading...</label>
                </div>
                <div class="col-2" v-if="!refreshing">
                    <button @click="refresh" class="btn btn-warning reset-btn">Refresh Data</button>
                </div>
                <div class="col-2" v-else>
                    <button class="btn btn-warning reset-btn" disabled>Refreshing...</button>
                </div>
            </div>
        </div>
        <div class="tableContainer upperTable" v-if="selectedPlayerStats && selectedPlayerStats.length">
            <DataTable :value="selectedPlayerStats" tableStyle="min-width: 50rem">
                <Column header="Remove">
                    <template #body="slotProps">
                        <button @click="removePlayer(slotProps.data.username)" class="btn btn-danger">Remove</button>
                    </template>
                </Column>
                <Column v-for="col of columns" sortable :key="col.field" :field="col.field" :header="col.header">
                    <template #body="slotProps">
                        <p :style="{ backgroundColor: get_color(col.field, slotProps.data[col.field]) }">
                            {{ typeof slotProps.data[col.field] === 'number' && slotProps.data[col.field] % 1 !== 0 ?
                                slotProps.data[col.field].toFixed(4) : slotProps.data[col.field] }}
                        </p>
                    </template>
                </Column>
            </DataTable>
        </div>
        <div class="buttonsContainer container" v-if="selectedPlayerStats && selectedPlayerStats.length">
            <div class="row">
                <div class="col-6" v-if="selectedPlayerStats && selectedPlayerStats.length">
                    <label for="search">Search: &nbsp;</label>
                    <input class="searchBar" v-model="search" placeholder="Search by username" @keyup="searchPlayers" />
                </div>
            </div>
        </div>
        <div class="tableContainer lowerTable" v-if="playerStats && playerStats.length">
            <DataTable :value="playerStats" tableStyle="min-width: 50rem">
                <Column header="Add">
                    <template #body="slotProps">
                        <button @click="addPlayer(slotProps.data.username)" class="btn btn-success"
                            v-if="!selectedPlayers.includes(slotProps.data.username)">Add</button>
                        <button @click="removePlayer(slotProps.data.username)" class="btn btn-danger"
                            v-else>Remove</button>
                    </template>
                </Column>
                <Column v-for="col of columns" sortable :key="col.field" :field="col.field" :header="col.header">
                    <template #body="slotProps">
                        {{ typeof slotProps.data[col.field] === 'number' && slotProps.data[col.field] % 1 !== 0 ?
                            slotProps.data[col.field].toFixed(4) : slotProps.data[col.field] }}
                    </template>
                </Column>
            </DataTable>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
import { DataTable } from 'primevue';
import { Column } from 'primevue';
import chroma from 'chroma-js';

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
            loadingFile: false,
            refreshing: false,
            mostRecentFileName: null,
            colorScale: chroma.scale(['red', '#444', 'green']),
            columns: [
                { field: "username", header: "Username" },
                { field: "profit_loss_per_game", header: "P/L per Game" },
                { field: "profit_loss_per_game_bb", header: "P/L per Game (BB)" },
                { field: "game_count", header: "Game Count" },
                { field: "bluffable_score", header: "Bluffable Score" },
                { field: "limper_score", header: "Limper Score" },
                { field: "aggressive_score", header: "Aggressive Score" },
                { field: "call_rate", header: "Calls Per Game" },
                { field: "raise_rate", header: "Raises Per Game" },
                { field: "preshowdown_fold_rate", header: "Fold Rate" }
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
        async handleFileUpload() {
            this.loadingFile = true
            this.gameFile = this.$refs.fileInput.files[0]
            const formData = new FormData()
            formData.append('file', this.gameFile)
            await axios.post(process.env.VUE_APP_REST_ENDPOINT + "/game-file", formData)
            this.playerStats = await this.getPlayerStats()
            this.allPlayerStats = this.playerStats
            this.mostRecentFileName = this.gameFile.name
            this.loadingFile = false
        },
        addPlayer(username) {
            this.selectedPlayers.push(username)
            this.selectedPlayerStats = this.allPlayerStats.filter(player => this.selectedPlayers.includes(player.username))
        },
        removePlayer(username) {
            this.selectedPlayers = this.selectedPlayers.filter(player => player !== username)
            this.selectedPlayerStats = this.allPlayerStats.filter(player => this.selectedPlayers.includes(player.username))
        },
        async refresh() {
            this.refreshing = true
            this.playerStats = await this.getPlayerStats()
            this.allPlayerStats = this.playerStats
            this.selectedPlayerStats = this.allPlayerStats.filter(player => this.selectedPlayers.includes(player.username))
            this.refreshing = false
        },
        get_color(col, value) {
            if (col.includes("count") || col.includes("user")) {
                return "#333"
            }
            let z_score = this.playerStats.filter(player => player[col] === value)[0][col + "_z_score"]
            return this.pickHex( z_score)
        },
        pickHex(z) {
            var weight = (z + 3) / 6
            let a = this.colorScale(weight)
            console.log(z)
            console.log(weight)
            console.log(a)
            return a;
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