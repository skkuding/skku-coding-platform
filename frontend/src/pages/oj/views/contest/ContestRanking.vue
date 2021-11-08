<template>
  <div class="contest-ranking-card font-bold">
    <div class="top-bar mb-4">
      <h2 class="title"> Standings </h2>
      <b-badge
        class="time-limit-container"
        variant="light"
        pill
      >
        <div v-if="remaintime.hour >= 0">
          <b-icon icon="clock-fill"/>
          {{ remaintime.hour + ':' + remaintime.min + ':' + remaintime.sec }}
        </div>
        <div v-else>Ended</div>
      </b-badge>
    </div>
    <div class="table">
      <b-table
        :items="contestRankingList"
        :fields="contestRankingListFields"
        :per-page="perPage"
        :current-page="currentPage"
        head-variant="light"
      >
        <template v-for="problem in contestProblemID"
          v-slot:[`cell(${problem})`]="data"
        >
          <div v-if="data.item[problem].is_ac === true" :key="problem">
            <div>{{ data.item[problem].score }}</div>
            <div>{{ getTimeformat(data.item[problem].ac_time) }}</div>
          </div>
          <div v-else-if="data.item[problem].problem_submission === '0'" :key="problem"> {{ '-' }}</div>
          <div v-else :key="problem" class="ac-false"> {{ '-' + data.item[problem].problem_submission }} </div>
        </template>
        <template #cell(id)="data">
          {{ data.value }}
        </template>
        <template #cell(accepted_number)="data">
          <div class="userAC">{{ data.value }}</div>
        </template>
        <template #cell(total_score)="data">
          <div class="userTotalscore">{{ data.value }}</div>
        </template>
      </b-table>
    </div>
    <div class="pagination">
      <b-pagination
        v-model="currentPage"
        :total-rows="contestRankingList.length"
        :per-page="perPage"
        limit="3"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
import api from '@oj/api'
import moment from 'moment'

export default {
  name: 'ContestRanking',
  data () {
    return {
      limit: 1000,
      total: 0,
      perPage: 20,
      currentPage: 1,
      contestID: '',
      contestRankingList: [],
      contestRankingListFields: [
        {
          key: 'id',
          label: '#'
        },
        {
          key: 'user.username',
          label: 'User',
          formatter: value => {
            return value.substr(0, 4) + '****' + value.substr(8, 2)
          }
        }
      ],
      contest: {},
      endtime: '',
      remaintime: {},
      contestProblems: [],
      contestProblemID: []
    }
  },
  async mounted () {
    this.contestID = this.$route.params.contestID
    await this.getContestDetail()
    await this.getContestProblems()
    for (const contestProblem of this.contestProblems) {
      this.contestProblemID.push((contestProblem.id) + '')
      this.contestRankingListFields.push({ key: contestProblem.id + '', label: contestProblem._id }) // table 에 표시되는건 display id
    }
    this.contestRankingListFields.push({ key: 'accepted_number', label: 'AC' })
    this.contestRankingListFields.push({ key: 'total_score', label: 'Total Score' })

    await this.getContestRanking()
    this.total = this.contestRankingList.length
    this.contestRankingList.problem = []
    this.setRankingList()
    setInterval(() => {
      this.calculateRemainTime()
    }, 1000)
  },
  methods: {
    async getContestDetail () {
      try {
        const res = await this.$store.dispatch('getContest')
        const data = res.data.data
        this.contest = data
        this.endtime = moment(data.end_time)
      } catch (err) {
      }
    },
    async getContestProblems () {
      try {
        const res = await this.$store.dispatch('getContestProblems')
        const data = res.data.data
        this.contestProblems = data
      } catch (err) {
      }
    },
    async getContestRanking () {
      try {
        const res = await api.getContestRanking(this.contestID, 1, 0, this.limit)
        const data = res.data.data.results
        this.contestRankingList = data
      } catch (err) {
      }
    },
    setRankingList () {
      for (const rank of this.contestRankingList) {
        for (const problem of this.contestProblemID) {
          if (Object.keys(rank.submission_info).includes(problem) === true) {
            this.$set(rank, problem, rank.submission_info[problem])
          } else {
            this.$set(rank, problem, { problem_submission: '0', is_ac: false })
          }
        }
      }
    },
    calculateRemainTime () {
      if (moment(this.endtime).isBefore(moment.now())) {
        this.$set(this.remaintime, 'hour', -1)
        return
      }
      var timeDiff = moment.duration(this.endtime.diff(moment.now())).asSeconds()
      var hour = parseInt(timeDiff / 3600)
      if (hour < 10) {
        hour = '0' + hour
      }
      this.$set(this.remaintime, 'hour', hour)
      timeDiff -= hour * 3600
      var min = parseInt(timeDiff / 60)
      if (min < 10) {
        min = '0' + min
      }
      this.$set(this.remaintime, 'min', min)
      timeDiff -= min * 60
      var sec = parseInt(timeDiff)
      if (sec < 10) {
        sec = '0' + sec
      }
      this.$set(this.remaintime, 'sec', sec)
    },
    getTimeformat (time) {
      const hour = parseInt(time / 60)
      time -= hour * 60
      const min = parseInt(time)
      return hour + ':' + min
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
      font-size: 14px;
      padding: 8px 50px;
      margin: 8px;
      color: #fff;
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
  .table-head{
    text-align: center;
  }
  .ac-false {
    color: #E9A05A;
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
