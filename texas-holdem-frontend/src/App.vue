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
  color: #FFF;
  background-color: #333;
  width: 100%;
  height: 100%;
}
body {
  width: 100%;
  height: 100vh;
  margin: 0; 
  display: flex;
  background-color: #333;
}
</style>
