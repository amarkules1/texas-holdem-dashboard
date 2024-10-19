<template>
  <HeaderComponent/>
  <CardStatsContainer/>
</template>

<script>
import CardStatsContainer from './components/CardStatsContainer.vue'
import HeaderComponent from './components/HeaderComponent.vue';

export default {
  name: 'App',
  components: {
    CardStatsContainer,
    HeaderComponent
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
  /* height: 100vh; */
  margin: 0; 
  display: flex;
  background-color: #333 !important;
  min-height: 100vh;
}
</style>
