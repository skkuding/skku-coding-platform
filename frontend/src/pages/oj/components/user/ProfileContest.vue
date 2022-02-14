<script src="./node_modules/chart.js/dist/chart.js"></script>
<template>
  <div class="profile-contest">
    <div class="section-title mt-4 mb-3">My Contest Rank Transition</div>

    <div class="rank-chart">
      <canvas id="myChart"></canvas>
    </div>

    <div class="sort-container">
      <b-dropdown text="Date" class="mr-4">
        <b-dropdown-item>All</b-dropdown-item>
        <b-dropdown-item>Rank</b-dropdown-item>
        <b-dropdown-item>Prize</b-dropdown-item>
      </b-dropdown>
    </div>

    <div class="table">
      <b-table
        hover
        :items="contests"
        :fields="fields"
        head-variant="light"
        @row-clicked="goContest"
      >
        <template #cell(start_time)="data">
          {{ getTimeFormat(data.value) }}
        </template>
        <!-- <template #cell(prize)="data"> {{ data.item.rank }}
          <b-icon
            icon="circle-fill"
            style="color: #ff6663"
            font-scale="1.2"
          ></b-icon>
          {{ data.item.prize }}
        </template> -->
      </b-table>
    </div>
    <div class="pagination">
      <Pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      limit="5"
      ></Pagination>
    </div>
  </div>
</template>

<script>
import api from '@oj/api'
import time from '@/utils/time'
import { Chart, registerables } from "chart.js";
import Pagination from "../Pagination.vue";
Chart.register(...registerables);

export default {
  name: 'ProfileContest',
  components: { Pagination },
  props: {},
  data() {
    return {
      rows: 100,
      currentPage: 1,
      perPage: 3,
      Chart,
      fields: [
        { label: "Date", key: "start_time" },
        { key: "title", label: "Title" },
        { key: "rank", label: "Rank" },
        { key: "percentage", label: "Prize" },
      ],
      contests: [
        {
          start_time: "2022-01",
          title: "skku contest",
          rank: "1",
          percentage: "33"
        }
      ],
    };
  },
  async mounted() {
    await this.getUserContestList()
    await this.drawChart();
  },
  methods: {
    drawChart() {
      const ctx = document.getElementById("myChart");
      const myChart = new Chart(ctx, {
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
    async getUserContestList () {
      try {
        const res = await api.getUserContestInfo()
        this.contests = res.data.data
      } catch (err) {
      }
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-MM-DD')
    },
    async goContest (item) {
      await this.$router.push({ name: 'contest-details', params: { contestID: item.id } })
    }
  },
  computed: {},
};
</script>

<style lang="scss" scoped>
.profile-contest {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.rank-chart {
  width: 90%;
}

.sort-container {
  width: 95%;
  margin-top: 30px;
  display: flex;
  justify-content: flex-end !important;
}

.table {
  width: 95%;
  margin: 0 auto;
  cursor: pointer;
}
.pagination {
  width: 95%;
  margin-right: 5%;
  margin-top: 20px;
  display: flex;
  justify-content: flex-end !important;
}
</style>
