<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <!-- <HoleCards/> -->
  <CardStatsContainer/>
</template>

<script>
// import HoleCards from './components/HoleCards.vue'
import CardStatsContainer from './components/CardStatsContainer.vue'

export default {
  name: 'App',
  components: {
    // HoleCards
    CardStatsContainer
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
