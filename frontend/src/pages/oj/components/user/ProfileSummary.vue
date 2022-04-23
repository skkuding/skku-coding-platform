<script src="./node_modules/chart.js/dist/chart.js"></script>
<template>
  <div class="profile-summary">
    <div class="subtitle">My Position</div>
    <div class="container">
      <p> <span class="font-red">670°C </span>Burning🔥</p>
      <p>for 23 days</p>
      <p style="margin-bottom: 10px;">5 more days for Roaring 🌋!</p>
      <div class="burning-container">
        <div id="burning-line">
          <div class="origin"></div>
          <div class="temperature"></div>
        </div>
        <div id="burning-gauge">
          <div class="gauge" v-for="(temper, idx) in temperatures" :key="idx">
            <b-icon
              icon="circle-fill"
              class="mr-2"
              :style="'color: gray; height: 20px;'"
            ></b-icon>
            <div class="scale"> {{temper[0]}} </div>
            <div class="scale"> {{temper[1]}} °C</div>
          </div>
        </div>
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
        <canvas id="barChart" style="min-height: 300px; max-height:300px;"></canvas>
      </div>
    </div>
    <div class="subtitle">Solved Problem</div>
    <div class="divided-container">
      <div class="left-box">
        <canvas id="doughnutChart" style="width:100%; height:auto;"></canvas>
      </div>
      <div class="right-box">
        <div class="table">
          <div class="problem-info">
            <div class="problem-level">
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
            </div>
            <div class="solved">
              <p>154 problems solved</p>
              <p>56.4% accuracy</p>
            </div>
          </div>
          <div class="problem-number">
            <div class="grid-set">
              <span v-for="(problem, idx) in problemsets" :key="idx">{{problem}}</span>
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
//import ChartDoughnutLabels from 'chartjs-plugin-doughnutlabel';
import { DIFFICULTY_COLOR } from '@/utils/constants';
Chart.register(...registerables);

export default {
  name: 'ProfileSummary',
  props: {},
  data () {
    return {
      Chart,
      temperatures: [
        ['Frozen', 0],
        ['Warm', 200],
        ['Hot', 400],
        ['Burning', 600],
        ['Roaring', 800]],
      problemsets: [10, 100, 1000, 1001, 1003, 1005, 1007, 1008]
    }
  },
  async mounted () {
    await this.drawStChart();
    await this.drawPbChart();
  },
  methods: {
    drawStChart(){
      const ctx = document.getElementById("barChart");
      const barChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: [1, 2, 3, 4],
          datasets: [
            {
              data: [15, 23, 31, 5],
              backgroundColor: ["#FF6663", "#FECC59", "#5ABF8A", "#74CFF3"],
              barThickness: 30,
            }
          ],
        },
        options: {
          responsive: true,
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
      const ctx = document.getElementById("doughnutChart");
      const doughnutChart = new Chart(ctx, {
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
  background-color:cornsilk;
  width: 100%;
  height: 250px;
  padding: 10px;
}

.burning-container {
  position: relative;
  padding-top: 20px;
  background-color: rgb(204, 237, 238);
  height: 100px;
}

#burning-line {
  position: absolute;
  z-index: 1;
  display: flex;
  flex-direction: row;
  background-color: #EAEAEA;
  width: 90%;
  height: 20px;
  border-radius: 5px;
}

#burning-line .origin {
  width: 20px;
  height: 20px;
  border-top-left-radius: 5px;
  border-bottom-left-radius: 5px;
  background: gray;
}

#burning-line .temperature {
  width: 72%;
  height: 20px;
  border-top-right-radius: 5px;
  border-bottom-right-radius: 5px;
  background-color: #FF6663;
}

#burning-gauge {
  position: relative;
  display: flex;
  flex-direction: row;
  z-index: 2;
  height: 100%;
}

#burning-gauge .gauge {
  width: 20%;
  flex-direction: column;
}

#burning-gauge .scale {
  font-size: 10px;
}

.font-red {
  color: red;
}

.divided-container {
  display: flex;
  flex-direction: row;
  background-color: honeydew;
}

.left-box {
  display: flex;
  width: 30%;
  height: auto;
  background-color: rgb(210, 231, 179);
  margin: 5px;
}

.right-box {
  width: 70%;
  background-color: rgb(210, 231, 179);
  margin: 5px;
}

.status-info {
  line-height: 450%;
  background-color: rgb(243, 192, 218);
  margin: 0 auto;
}

.table {
  display: flex;
  flex-direction: row;
  border-top: 1px solid #7A7C7B;
  border-bottom: 1px solid #7A7C7B;
  background-color: whitesmoke;
  width: 90%;
  height: 100%;
  margin-left: 10px;
}

.problem-info {
  display: flex;
  flex-direction: column;
  background-color: #F9F9F9;
  width: 30%;
  height: auto;
  padding: 10px;
}

.problem-level {
  background-color: lightpink;

}

.solved {
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: lightskyblue;
  height: 100%;
}

.problem-number {
  background-color: rgb(238, 238, 174);
  width: 70%;
  height: 100%;
  min-height: 150px;
  padding: 10px;
}

.grid-set {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  text-align: center;
  background-color: rgb(174, 228, 228);
  height: auto;
}

</style>
