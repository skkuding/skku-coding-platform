<template>
  <div class="contest-ranking-card font-bold">
    <div class="top-bar mb-4">
      <!-- <h2 class="title"> {{ contest.title + 'Standings' }} </h2> -->
      <h2 class="title"> Standings </h2>
      <b-badge
        class="time-limit-container"
        variant="light"
        size="sm"
      >
        limit time
      </b-badge>
    </div>
    <div class="table">
      <b-table
        :items="contestRankingList"
        :fields="contestRankingListFields"
        head-variant="light"
      >
        <template #cell(A)="data">
          <row class="userscore">{{ data.value.score }}</row>
          <row class="usertime"> {{ data.value.time }} </row>
        </template>
        <template #cell(B)="data">
          <row class="userscore"> {{ data.value.score }} </row>
          <row class="usertime"> {{ data.value.time }} </row>
        </template>
        <template #cell(C)="data">
          <row class="userscore"> {{ data.value.score }} </row>
          <row class="usertime"> {{ data.value.time }} </row>
        </template>
        <template #cell(AC)="data">
          <div class="userAC">{{ data.value }}</div>
        </template>
        <template #cell(totalscore)="data">
          <div class="userTotalscore">{{ data.value }}</div>
        </template>
        <template #thead-top="">
          <b-tr>
            <b-th colspan="2"><span class="sr-only">Ranking and Username</span></b-th>
            <b-th>A</b-th>
            <b-th>B</b-th>
            <b-th>C</b-th>
            <b-th centered colspan="2">Total</b-th>
          </b-tr>
        </template>
      </b-table>
    </div>
    <!-- <div class="pagination">
      <b-pagination
        v-model="currentPage"
        :total-rows="contestProblems.length"
        :per-page="perPage"
        limit="3"
      ></b-pagination>
    </div> -->
  </div>
</template>

<script>
import api from '@oj/api'

export default {
  name: 'ContestRanking',
  data () {
    return {
      contestID: '',
      contestRankingList: [
        {
          rank: 1,
          user_name: '2018310000',
          A: { totalscore: 500, score: 300, time: '00:02' },
          B: { totalscore: 500, score: 700, time: '00:30' },
          C: { totalscore: 500, score: 1500, time: '01:50' },
          AC: 3,
          totalscore: 2500
        },
        {
          rank: 2,
          user_name: '2018311111',
          A: { totalscore: 500, score: 300, time: '00:02' },
          B: { totalscore: 500, score: 600, time: '00:30' },
          C: { totalscore: 500, score: 0, time: '0' },
          AC: 2,
          totalscore: 900
        },
        {
          rank: 3,
          user_name: '2018312222',
          A: { totalscore: 500, score: 200, time: '00:02' },
          B: { totalscore: 500, score: 0, time: '0' },
          C: { totalscore: 500, score: 0, time: '0' },
          AC: 1,
          totalscore: 200
        }
      ],
      contestRankingListFields: [
        {
          key: 'rank',
          label: '#'
        },
        {
          key: 'user_name',
          label: 'User',
          formatter: value => {
            return value.substr(0, 4) + '****' + value.substr(8, 2)
          }
        }, 'A', 'B', 'C', 'AC', 'totalscore'
      ]
    }
  },
  async mounted () {
    this.contestID = this.$route.params.contestID
    await this.getContestRanking()
  },
  methods: {
    async getContestRanking () {
      try {
        const res = await api.getContestRanking(this.contestID, 1)
        console.log(res)
      } catch (err) {
        console.log('error')
        console.log(err)
      }
    }
  },
  computed: {
  },
  watch: {
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .top-bar {
    margin-top: 40px;
    margin-left: 68px;
    width: 90%;
    display: flex;
    justify-content: space-between;
    .time-limit-container {
      font-size: 12px;
      padding: 6px 10px;
      color: #4F4F4F;
      background-color: #E9A05A;
    }
  }
  .title {
    color: #7C7A7B;
    display:inline;
    position:relative;
    // top:36px;
  }
  .contest-ranking-card {
    margin: 0 auto;
    width: 70%;
    font-family: Manrope;
  }
  .table{
    width: 95% !important;
    margin: 0 auto;
  }
  .userscore{
    color: #8DC63F;
  }
  .usertime {
    font-size: 10px;
  }
  .userTotalscore, .userAC{
    color: #3391E5;
  }
  div {
    &.pagination{
      margin-right: 5%;
      margin-top: 20px;
      display: flex;
      justify-content: flex-end;
    }
  }
</style>
