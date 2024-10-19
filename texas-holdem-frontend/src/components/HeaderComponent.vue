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
                    It provides details like the current win rate and parcentile, as well as the Sklansky ranking for your hole cards.
                    The "Modified Sklansky" values are based on a set of game simulations that I used to recalculate Sklansky rankings. YMMV.
                </p>
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
    width: 50%;
    background-color: #000;
    position: fixed;
    top: 25%;
    left: 25%;
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
    margin: 20px;
    padding: 20px;
    color: #fff;
}
</style>