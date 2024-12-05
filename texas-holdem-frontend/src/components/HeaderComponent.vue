<template>
    <div class="header">
        <div class="container">
            <div class="row">
                <div class="col-sm-2"></div>
                <div class="col-sm-8">
                    <h1>Texas Hold'em Dashboard</h1>
                </div>
                <div class="col-sm-2">
                    <div class="buttons">
                        <FontAwesomeIcon :icon="faInfoCircle" size="2x" @click="showInfo = !showInfo" />
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="info-bg" v-if="showInfo">
        <div class="info-container">
            <div class="info-close" @click="showInfo = !showInfo">
                <FontAwesomeIcon :icon="faTimes" size="lg" />
            </div>
            <div class="info-text">
                <h3>Instructions</h3>
                <p>Welcome to Texas Hold'em! This dashboard provides statistics about your poker hand at any point in the game.
                    <br/>
                    To see stats about a particular scenario, select your hole (hand) cards and any known community cards. 
                    The following statistics will be displayed:</p>
                    <ul class="info-descriptions list-group">
                        <li class="list-group-item">
                            <strong>Current Win Rate:</strong> Expected win rate against (as a proportion) random hands, 
                            based on the number of players, your hand, and any known community cards. This win rate assumes 
                            other players have a random hand, which may become a less accurate estimate as the game progresses 
                            and players with worse hands fold, but it still gives you an idea of the relative strength of your hand.
                        </li>
                        <li class="list-group-item">
                            <strong>Kelly Criterion:</strong> The percentage of your chips that you should bet based on the strength of your hand.
                            The <a href="https://en.wikipedia.org/wiki/Kelly_criterion">Kelly Criterion</a> is based on the number of players and the current win rate, so the same caveats apply. You may find
                            that a smaller amount (e.g. 1/2 or 1/3  of the Kelly Criterion) is a better bet.
                        </li>
                        <li class="list-group-item">
                            <strong>Percentile:</strong> Relative ranking (as a percentile) against all other hands at the current point.
                        </li>
                        <li class="list-group-item">
                            <strong>Sklansky Rank:</strong> Number from 1 to 9 indicating the strength of your hand pre-flop, based on <a href="https://en.wikipedia.org/wiki/Texas_hold_%27em_starting_hands#Sklansky_hand_groups">Sklansky Hand Groups</a>.
                        </li>
                        <li class="list-group-item">
                            <strong>Sklansky Position:</strong> Description of the Sklansky hand rank, the position and scenario in which you should play it.
                        </li>
                    </ul>
                    <br/>
                <p>Author: <a href="http://marqless.xyz">Alex Markules</a></p>
            </div>

        </div>

    </div>
</template>

<script setup>
import { ref } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faInfoCircle, faTimes } from '@fortawesome/free-solid-svg-icons'

const showInfo = ref(false)
</script>
<style scoped>
.header {
    background-color: #000;
    padding-top: 10px;
    padding-bottom: 10px;
    margin-bottom: 20px;
    display: inline-block;
    width: 100%;
}

.buttons {
    padding-top: 12px;
}

.info-bg {
    display: block;
    /* Hidden by default */
    position: fixed;
    /* Stay in place */
    z-index: 1;
    /* Sit on top */
    left: 0;
    top: 0;
    width: 100%;
    /* Full width */
    height: 100%;
    /* Full height */
    overflow: auto;
    /* Enable scroll if needed */
    background-color: rgb(0, 0, 0);
    /* Fallback color */
    background-color: rgba(0, 0, 0, 0.4);
    /* Black w/ opacity */
}

.info-container {
    border: 3px solid #fff;
    border-radius: 10px;
    width: 70%;
    background-color: #000;
    position: fixed;
    top: 25%;
    left: 15%;
    opacity: 1;
    z-index: 1000;
}

.info-close {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 24px;
    color: #fff;
    cursor: pointer;
    transition: opacity 0.3s;
}
.info-text{
    margin: 40px 10px 10px 10px;
    padding: 20px;
    color: #fff;
    overflow: auto;
    max-height: 400px;
}
</style>