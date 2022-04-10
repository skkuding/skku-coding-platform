<template>
  <div class="contest-ranking-card font-bold">
    <Table
      text="No Standings"
      :items="contestRankingList"
      :fields="contestRankingListFields"
      :per-page="perPage"
      :current-page="currentPage"
      class="text-center"
    >
      <template v-for="problem in contestProblemID"
        v-slot:[`${problem}`]="data"
      >
        <div v-if="data.row[problem].is_ac === true" :key="problem">
          <div class="text-green text-center">{{ data.row[problem].problem_submission }}</div>
          <div v-if="contest.rank_penalty_visible" class="text-xs">{{ parseInt(data.row[problem].penalty) }}</div>
        </div>
        <div v-else-if="data.row[problem].problem_submission === '0'"
          :key="problem"
        >
          {{ '-' }}
        </div>
        <div v-else :key="problem" class="text-text-title"> {{ '-' + data.row[problem].problem_submission }} </div>
      </template>
      <template v-slot:id="data">
        {{ data.index + (currentPage - 1) * perPage + 1 }}
      </template>
      <template v-slot:username="data" class="w-1/2">
        <div class="text-left">{{ data.row.username }}</div>
      </template>
      <template v-slot:accepted_number="data">
        <div class="text-blue">{{ data.row.accepted_number }}</div>
        <div v-if="contest.rank_penalty_visible" class="text-xs">{{ data.row.total_penalty }}</div>
      </template>
    </Table>
    <div class="table-footer">
      <b-icon icon="question-circle" id="standings-info" style="margin-right: 50px;"/>
      <b-popover
        target="standings-info"
        title="How to read?"
        placement="bottom"
        triggers="hover focus"
      >
        <img style="width: 200px; height: auto;" src="@/assets/standing.png"/>
      </b-popover>
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
import Table from '@oj/components/Table.vue'

export default {
  name: 'ContestRanking',
  components: {
    Table
  },
  data () {
    return {
      limit: 200,
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
          key: 'username',
          label: 'User'
        }
      ],
      contest: {},
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
    this.contestRankingListFields.push({ key: 'accepted_number', label: 'AC' })

    await this.getContestRanking()
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
  .table-footer{
    margin-right: 5%;
    margin-left: 5%;
    margin-top: 20px;
    display: flex;
    justify-content: space-between
  }
  .font-bold {
    font-family: manrope_bold;
  }
</style>
