<script src="./node_modules/chart.js/dist/chart.js"></script>
<template>
  <div class="profile-summary">
    <div class="subtitle">My Position</div>
    <div class="container">
      <p> <span class="font-red">670°C </span>Burning🔥</p>
      <p>for 23 days</p>
      <div class="burning-container">
        <p>5 more days for Roaring 🌋!</p>
        <div id="burning-line"></div>
      </div>
    </div>
    <div class="subtitle">Position History</div>
    <div class="divided-container">
      <div class="left-box">
        <div class="status-info">
          <p>Roaring🌋 : 15 days</p>
          <p class="font-red">Burning🔥 : 23 days</p>
          <p>Hot🕯 : 31 days</p>
          <p>Warm🌸 : 5 days</p>
        </div>
      </div>
      <div class="right-box">
        <div class="status-chart">
          <canvas id="stChart"></canvas>
        </div>
      </div>
    </div>
    <div class="subtitle">Solved Problem</div>
    <div class="divided-container">
      <div class="left-box">
        <canvas id="pbChart"></canvas>
      </div>
      <div class="right-box">
        <div class="table">
          <div class="problem-info">
            <p>
              <span>
                <b-icon
                  icon="circle-fill"
                  class="mr-2"
                  :style="'color:' + difficultyColor('Level4')"
                ></b-icon>
              </span>
              Level4
            </p>
            <p>154 problems solved</p>
            <p>56.4% accuracy</p>
          </div>
          <div class="grid-set">
            <div v-for="(problem, idx) in problemsets" :key="idx" style="grid-column: idx">
              {{problem}}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
import ChartDataLabels from 'chartjs-plugin-datalabels';
//import ChartDoughnutLabels from 'chartjs-plugin-doughnutlabel'
import { DIFFICULTY_COLOR } from '@/utils/constants'
Chart.register(...registerables);

export default {
  name: 'ProfileSummary',
  props: {},
  data () {
    problemsets: [1001, 1002, 1003, 1004, 1005]
    return {
      Chart,
    }
  },
  async mounted () {
    await this.drawStChart();
    await this.drawPbChart();
  },
  methods: {
    drawStChart(){
      const ctx = document.getElementById("stChart");
      const stChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: [1, 2, 3, 4],
          datasets: [
            {
              data: [15, 23, 31, 5],
              backgroundColor: ["#FF6663", "#FECC59", "#5ABF8A", "#74CFF3"],
              barThickness: 30,
            },
            {
              data: [50-15, 50-23, 50-31, 50-5],
              backgroundColor: "#EAEAEA",
              barThickness: 30,
            }
          ],
        },
        options: {
          plugins: {
            legend: {
              display: false,
              position: 'right',
            }
          },
          indexAxis: 'y',
          scales: {
            y: {
              stacked: true,
              ticks: { display: false },
              grid: { display: false }
            },
            x: {
              stacked: true,
              ticks: { display: false },
              grid: { display: false }
            }
          }
        }
      });
    },
    // Draw problem doughnut chart
    drawPbChart() {
      const ctx = document.getElementById("pbChart");
      const pbChart = new Chart(ctx, {
        type: 'doughnut',
        plugins: [ChartDataLabels],
        data: {
          datasets: [
            {
              labels: [1, 2, 3, 4, 5, 6, 7],
              data: [10, 20, 30, 40, 50, 60, 70],
              backgroundColor: [1, 2, 3, 4, 5, 6, 7].map((i) => DIFFICULTY_COLOR['Level'+i]),
              borderWidth: 0
            }
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false,
              position: 'top',
            },
            datalabels: {
              formatter: function(val, ctx) {
                return ctx.dataset.labels[ctx.dataIndex];
              },
              font: { size: 15 }
            },
            // doughnutlabel: {
            //   labels: {
            //     text: 'title'
            //   }
            // }
          }
        }
      });
    },
    difficultyColor (value) {
      return DIFFICULTY_COLOR[value]
    },
  },
  computed: {}
}
</script>

<style lang="scss" scoped>
.profile-summary {
  margin:50px;
}

.subtitle {
  margin: 10px;
}

.container {
  //background-color:cornsilk;
  width: 100%;
  height: 250px;
  padding: 10px;
}

.burning-container {
  margin-top: 20px;
  //background-color: rgb(204, 237, 238);
  height: 100px;
}

.font-red {
  color: red;
}

.divided-container {
  display: flex;
  flex-direction: row;
  height: 250px;
  //background-color: honeydew;
}

.left-box {
  display: flex;
  width: 30%;
  height: 100%;
  //background-color: rgb(210, 231, 179);
  margin: 5px;
}

.right-box {
  width: 70%;
  height: 100%;
  //background-color: rgb(210, 231, 179);
  margin: 5px;
}

.status-info {
  line-height: 360%;
  //background-color: rgb(243, 192, 218);
  margin: 0 auto;
}

.status-chart {
  width: 100%;
  height: 100%;
  //background-color: wheat;
}

#stChart, #pbChart {
  width: 100% !important;
  height: 100% !important;
}

.table {
  display: flex;
  flex-direction: row;
  border-top: 1px solid #7A7C7B;
  border-bottom: 1px solid #7A7C7B;
  //background-color: whitesmoke;
  width: 90%;
  height: 200px;
  margin-left: 10px;
}

.problem-info {
  background-color: #F9F9F9;
  width: 30%;
  height: 100%;
  padding: 10px;
}

.grid-set {
  display: grid;
  grid-template-rows: repeat(3, 1fr);
  grid-template-columns: (10, 1fr);
  gap: 10px;
  //background-color: rgb(174, 228, 228);
  width: 70%;
  height: 100%;
  color: black;
}

.item:nth-child(1) {
  grid-column: 1;
}

</style>
