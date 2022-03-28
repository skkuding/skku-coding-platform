<script src="./node_modules/chart.js/dist/chart.js"></script>
<template>
  <div class="profile-history">
    test
    <canvas id="problemNumberChart"></canvas>
    aa
    <!--
      <canvas id="temperatureChart"></canvas>
      <canvas id="rankChart"></canvas>
    -->
  </div>
</template>

<script>
import api from '@oj/api'
import time from '@/utils/time'
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  name: 'ProfileHistory',
  props: {},
  data() {
    return {
    };
  },
  async mounted() {
    await this.getUserHistory()
    await this.drawChart();
  },
  methods: {
    underwayClass(item, type) {
      if(!item || type!=='row') return
      if(item.rank < 0) {
        item.rank = "-"
        item.percentage = "-"
        return 'underwayClass'
      }
    },
    drawChart() {
      const ctx1 = document.getElementById("problemNumberChart");
      const problemNumberChart = new Chart(ctx1, {
        type: "line",
        data: {
          datasets: [
            {
              label: "# of solved problems",
              data: [{
                x: '2021-11-06',
                y: 50
                },
                {
                  x: '2021-11-07',
                  y: 60
                },
                {
                  x: '2021-11-07',
                  y: 20
                }],
            },
          ],
        },
        options: {
        }
      });
      const ctx2 = document.getElementById("temperatureChart");
      const temperatureChart = new Chart(ctx2, {
        type: "line",
        data: {
          labels: this.contests.map(x=>x.title),
          datasets: [
            {
              label: "Me",
              data: this.contests.map(x=>x.percentage),
              borderColor: "#FF6663",
              backgroundColor: "#FF6663",
              yAxisId: 'y',
            },
          ],
        },
        options: {
          scales: {
            y: {
              suggestedMin: 0,
              suggestedMax: 100,
              reverse: true
            }
          }
        }
      });
      const ctx3 = document.getElementById("rankChart");
      const rankChart = new Chart(ctx3, {
        type: "line",
        data: {
          labels: this.contests.map(x=>x.title),
          datasets: [
            {
              label: "Me",
              data: this.contests.map(x=>x.percentage),
              borderColor: "#FF6663",
              backgroundColor: "#FF6663",
              yAxisId: 'y',
            },
          ],
        },
        options: {
          scales: {
            y: {
              suggestedMin: 0,
              suggestedMax: 100,
              reverse: true
            }
          }
        }
      });
    },
    async getUserHistory () {
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-MM-DD')
    },
  },
  computed: {}
};
</script>

<style lang="scss" scoped>
</style>
