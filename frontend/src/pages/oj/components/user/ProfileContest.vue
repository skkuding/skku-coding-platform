<script src="./node_modules/chart.js/dist/chart.js"></script>
<template>
  <div class="profile-contest">
    <div class="section-title mt-4 mb-3">My Contest Rank Transition</div>

    <div class="rank-chart">
      <canvas id="myChart"></canvas>
    </div>

    <div class="sort-container">
      <b-dropdown :text="priority" class="mr-4">
        <b-dropdown-item @click="sortBy('all')">all</b-dropdown-item>
        <b-dropdown-item @click="sortBy('rank')">rank</b-dropdown-item>
        <b-dropdown-item @click="sortBy('date')">date</b-dropdown-item>
        <b-dropdown-item @click="sortBy('title')">title</b-dropdown-item>
        <b-dropdown-item @click="sortBy('percentage')">prize</b-dropdown-item>
      </b-dropdown>
    </div>

    <div class="table">
      <b-table
        hover
        :items="contests"
        :fields="fields"
        head-variant="light"
        @row-clicked="goContest"
        :tbody-tr-class="underwayClass"
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
      limit="1"
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
      priority: 'all',
      Chart,
      fields: [
        { label: "Date", key: "start_time" },
        { key: "title", label: "Title" },
        { key: "rank", label: "Rank" },
        { key: "percentage", label: "Prize" },
      ],
      contests: [],
    };
  },
  async mounted() {
    await this.getUserContestList()
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
        const offset = (this.page - 1) * this.limit
        const res = await api.getUserContestInfo(offset, this.limit, {
          priority: this.priority === 'all' || this.priority === 'date' ? 'start_time' : this.priority,
          page: this.page
        })
        this.contests = res.data.data
      } catch (err) {
      }
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-MM-DD')
    },
    async goContest (item) {
      await this.$router.push({ name: 'contest-details', params: { contestID: item.id } })
    },
    async sortBy(priority){
      this.priority = priority
      await this.getUserContestList()
    },
  },
  computed: {}
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

.underwayClass {
  backgroundColor: red;
}

.pagination {
  width: 95%;
  margin-right: 5%;
  margin-top: 20px;
  display: flex;
  justify-content: flex-end !important;
}
</style>
