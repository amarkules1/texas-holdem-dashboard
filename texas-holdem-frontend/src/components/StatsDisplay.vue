<template>
  <div class="statsDisplay">
    <div class="stats">
      <div class="container statsContainer">
        <div v-if="perf && perf.current_win_rate">
          <div>
            <div class="row">
              <div class="col-sm">
                <h5>Current Win Rate: {{ perf.current_win_rate ? perf.current_win_rate.toFixed(3) : "N/A" }}</h5>
              </div>
              <div class="col-sm">
                <h5>Kelly Criterion: {{perf.ideal_kelly_max > 0 ? (100 * perf.ideal_kelly_max).toFixed(3) : 0.0 }}%</h5>
              </div>
              <div class="col-sm">
                <h5>Percentile: {{ perf.percentile ? perf.percentile.toFixed(3) : "N/A" }}%</h5>
              </div>
            </div>
          </div>
          <div>
            <div class="row" v-if="cardCount < 5">
              <div class="col-sm">
                <h5>Sklansky Rank: {{ perf.sklansky }}</h5>
              </div>
              <div class="col-sm">
              </div>
              <div class="col-sm">
                <h5>Sklansky Playability: {{ perf.sklansky_position }}</h5>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'StatsDisplay',
  props: {
    perf: Object,
    cardCount: Number
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