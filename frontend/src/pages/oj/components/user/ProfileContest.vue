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
      <b-table hover :items="items" :fields="fields" head-variant="light">
        <template #cell(title)="data">{{ data.item.title }}</template>
        <template #cell(prize)="data">
          <b-icon
            icon="circle-fill"
            style="color: #ff6663"
            font-scale="1.2"
          ></b-icon>
          {{ data.item.prize }}
        </template>
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
        { key: "date", label: "Date" },
        { key: "title", label: "Title" },
        { key: "rank", label: "Rank" },
        { key: "prize", label: "Prize" },
      ],
      items: [
        {
          date: "2021-12-31",
          title: "SKKU Coding Platform 모의대회",
          rank: "1",
          prize: "Top3",
        },
        {
          date: "2021-12-31",
          title: "SKKU Coding Platform 2차 모의대회",
          rank: "2",
          prize: "Top5",
        },
        {
          date: "2021-12-31",
          title: "SKKU Coding Platform 3차 모의대회",
          rank: "100",
          prize: "Top2",
        },
      ],
    };
  },
  async mounted() {
    this.drawChart();
  },
  methods: {
    drawChart() {
      const ctx = document.getElementById("myChart");
      const myChart = new Chart(ctx, {
        type: "line",
        data: {
          labels: [
            "Contest1",
            "Contest2",
            "Contest3",
            "Contest4",
            "Contest5",
            "Contest6",
          ],
          datasets: [
            {
              label: "Me",
              data: [30, 85, 20, 100, 50, 1],
              borderColor: "#FF6663",
              backgroundColor: "#FF6663",
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
          },
        },
      });
    },
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
  width: 80%;
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
