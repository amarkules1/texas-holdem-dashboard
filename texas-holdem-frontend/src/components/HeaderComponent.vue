<template>
    <div class="header">
        <div class="container">
            <div class="centering">
                <router-link class="title" to="/home">
                    <img class="headerImage" src="../../public/web-app-manifest-192x192.png" alt="CasinoSolver"
                        width="100" height="100" />
                    <h1 class="headerText">CasinoSolver</h1>
                </router-link>
            </div>
            <div class="buttons">
                <button class="navbar-toggler col-sm-1 headerButton" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false"
                    aria-label="Toggle navigation" @click="showMenu = !showMenu">
                    <FontAwesomeIcon :icon="faBars" size="2x" v-if="!showMenu" />
                    <FontAwesomeIcon :icon="faTimes" size="2x" v-else />
                </button>
            </div>
            <div class="collapse navbar-collapse navMenuItems" id="navbarTogglerDemo02">
                <ul class="navbar-nav ms-auto ">
                    <li class="nav-item">
                        <router-link class="nav-link" active-class="active" to="/home">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" active-class="active" to="/hand-comparison">Hand
                            Comparison</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/outs-tracker">Outs Tracker</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/blackjack-strategy">Blackjack Strategy</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/blackjack-quiz">Blackjack Quiz</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/bet-analysis">Bet Analysis</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" active-class="active" to="/resources">Resources</router-link>
                    </li>
                </ul>
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faTimes, faBars } from '@fortawesome/free-solid-svg-icons'

const showMenu = ref(false)
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

.centering {
    /* margin: auto; */
    width: 350px;
    height: 100%;
}

.headerButton {
    margin-left: 10px;
    margin-top: 16px;
}

.buttons {
    float: right;
}

.headerImage {
    float: left;
}

.headerText {
    float: left;
    margin-top: 24px;
}

.title {
    margin: auto;
    color: #fff;
    text-align: center;
    text-decoration: none !important;
}

.buttons {
    padding-top: 12px;
}

.navMenuItems {
    clear: both;
}
</style>