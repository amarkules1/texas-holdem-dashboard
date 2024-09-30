<template>
    <div class="statsContainer">
  <div class="stats">
    <h3>Hand Performance</h3>
    <ul>
      <li>
        Pre-Flop Win Rate: {{ perf.win_rate ? perf.win_rate.toFixed(3) : "N/A" }}
      </li>
      <li>
        Current Win Rate: {{ perf.current_win_rate ? perf.current_win_rate.toFixed(3) : "N/A" }}
      </li>
      <li>
        Percentile: {{ perf.percentile ? perf.percentile.toFixed(3) : "N/A" }}%
      </li>
      <li>
        Sklansky Rank: {{ perf.sklansky }}
      </li>
      <li>
        Sklansky Playability: <strong>{{ perf.sklansky_position }}</strong>
      </li>
      <li>
        Modified Sklansky Rank: {{ perf.modified_sklansky }}
      </li>
      <li>
        Modified Sklansky Playability: <strong>{{ perf.modified_sklansky_position }}</strong>
      </li>
    </ul>
  </div>
  </div>
</template>
<script>
export default {
    name: 'StatsDisplay',
    props: {
        perf: Object
    }
}
</script>