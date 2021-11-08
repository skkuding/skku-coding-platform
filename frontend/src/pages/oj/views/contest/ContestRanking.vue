<template>
  <div class="contest-ranking-card font-bold">
    <div class="top-bar mb-4">
      <h2 class="title"> {{ contest.title }} </h2>
      <status-badge
        :status_name="contestStatus.name"
        :status_color="contestStatus.color"
        :status_endtime="contest.end_time"
      ></status-badge>
    </div>

    <b-navbar class="contest-tab" sticky-top style="height: 100%;">
      <b-navbar-nav class="mx-auto" align="center">
        <b-nav-item class="contest__menu">
          <router-link class="nav-link" :to="{ name: 'contest-details', param: { contest_id : contestID }}">Top</router-link>
        </b-nav-item>
        <b-nav-item class="contest__menu">
          <router-link class="nav-link" :to="{ name: 'contest-problems', param: { contest_id : contestID }}">Problems</router-link>
        </b-nav-item>
        <b-nav-item class="contest__menu">
          <router-link class="nav-link" :to="{ name: 'contest-ranking', param: { contest_id : contestID }}">Standings</router-link>
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>

    <div class="table">
      <b-table
        :items="contestRankingList"
        :fields="contestRankingListFields"
        :per-page="perPage"
        :current-page="currentPage"
        head-variant="light"
        class="text-center"
      >
        <template v-for="problem in contestProblemID"
          v-slot:[`cell(${problem})`]="data"
        >
          <div v-if="data.item[problem].is_ac === true" :key="problem">
            <div class="user-score">{{ parseInt(data.item[problem].score) }}</div>
            <div class="user-time">{{ getTimeformat(data.item[problem].ac_time) }}</div>
          </div>
          <div v-else-if="data.item[problem].problem_submission === '0'"
            :key="problem"
          >
            {{ '-' }}
          </div>
          <div v-else :key="problem" class="ac-false"> {{ '-' + data.item[problem].problem_submission }} </div>
        </template>
        <template #cell(id)="data">
          {{ data.index + 1 }}
        </template>
        <template #cell()="data">
          <div class="user-name">{{ data.value }}</div>
        </template>
        <template #cell(accepted_number)="data">
          <div class="user-AC">{{ data.value }}</div>
          <div class="user-penalty">{{ data.item.total_penalty }}</div>
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
import StatusBadge from '../../components/StatusBadge.vue'
import { mapState, mapGetters } from 'vuex'
import { CONTEST_STATUS_REVERSE } from '@/utils/constants'

export default {
  components: { StatusBadge },
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
      this.contestRankingListFields.push({ key: contestProblem.id + '', label: contestProblem._id })
    }
    this.contestRankingListFields.push({ key: 'accepted_number', label: '' })

    await this.getContestRanking()
    console.log(this.contestRankingList)
    this.total = this.contestRankingList.length
    this.contestRankingList.problem = []
    this.setRankingList()
  },
  methods: {
    async getContestDetail () {
      try {
        const res = await this.$store.dispatch('getContest')
        const data = res.data.data
        this.contest = data
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
    getTimeformat (time) {
      const hour = this.checkNumberformat(parseInt(time / 60))
      time -= hour * 60
      const min = this.checkNumberformat(parseInt(time))
      return hour + ':' + min
    },
    checkNumberformat (num) {
      if (num < 10) {
        return '0' + num
      } else {
        return num
      }
    }
  },
  computed: {
    ...mapState({
      contest: state => state.contest.contest
    }),
    ...mapGetters(['contestStatus']),
    contestStatus () {
      return {
        name: CONTEST_STATUS_REVERSE[this.contest.status].name,
        color: CONTEST_STATUS_REVERSE[this.contest.status].color
      }
    }
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
  .user-name {
    width: 120px;
  }
  .ac-false {
    color: #E9A05A;
  }
  .user-time, .user-penalty {
    font-size: 12px;
  }
  .user-AC{
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
  .font-bold {
    font-family: manrope_bold;
  }
</style>
