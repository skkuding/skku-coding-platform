<template>
  <div class="contest-ranking-card font-bold">
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
            <div class="user-time">{{ data.item[problem].problem_submission }}</div>
            <div class="user-penalty">{{ parseInt(data.item[problem].penalty) }}</div>
          </div>
          <div v-else-if="data.item[problem].problem_submission === '0'"
            :key="problem"
          >
            {{ '-' }}
          </div>
          <div v-else :key="problem" class="ac-false"> {{ '-' + data.item[problem].problem_submission }} </div>
        </template>
        <template #cell(id)="data">
          {{ data.index + (currentPage - 1) * perPage + 1 }}
        </template>
        <template #cell()="data">
          <div class="user-name">{{ data.value }}</div>
        </template>
        <template #cell(accepted_number)="data">
          <div class="user-AC">{{ data.value }}</div>
          <div class="user-total-penalty">{{ data.item.total_penalty }}</div>
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

export default {
  name: 'ContestRanking',
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
          key: 'user.username',
          label: 'User',
          formatter: value => {
            return value.substr(0, 4) + '****' + value.substr(8, 2)
          }
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
  .user-name {
    width: 120px;
  }
  .ac-false {
    margin: auto 0;
    color: #9da6af;
  }
  .user-penalty {
    font-size: 12px;
  }
  .user-time {
    color: #8dc63f;
  }
  .user-total-penalty {
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
