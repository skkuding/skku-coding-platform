<template>
  <div class="contest-problem-list-card font-bold">
    <b-button v-if="showProblemBankStartBtn" @click="startProblemBankContest(contest)" style="width:100%">Start Contest</b-button>
    <div v-else>
      <Table
        hover
        :items="contestProblems"
        :fields="contestProblemListFields"
        :per-page="perPage"
        :current-page="currentPage"
        @row-clicked="goContestProblem"
      >
        <template v-slot:_id="data">
          {{data.row._id}}
        </template>
        <template v-slot:title="data">
          {{data.row.title}}
          <b-icon
            icon="check2-circle"
            style="color: #8DC63F;"
            font-scale="1.2"
            v-if="data.row.my_status===0"></b-icon>
        </template>
      </Table>
      <div class="pagination">
        <b-pagination
          v-model="currentPage"
          :total-rows="contestProblems.length"
          :per-page="perPage"
          limit="3"
        ></b-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { types } from '@/store'
import { ProblemMixin } from '@oj/components/mixins'
import Table from '@oj/components/Table.vue'
import api from '@oj/api'

export default {
  name: 'ContestProblemList',
  components: {
    Table
  },
  mixins: [ProblemMixin],
  data () {
    return {
      // ACMTableColumns: [
      //   {
      //     label: '#',
      //     key: 'id',
      //     sortType: 'asc',
      //     width: 150
      //   },
      //   {
      //     label: this.$i18n.t('m.Title'),
      //     key: 'title'
      //   }
      // ],
      limit: 200,
      total: 0,
      perPage: 10,
      currentPage: 1,
      contestID: '',
      contest: {},
      contestProblems: [],
      contestProblemListFields: [
        {
          label: '#',
          key: '_id'
        },
        {
          label: 'Title',
          key: 'title'
        }
      ]
    }
  },
  async mounted () {
    this.contestID = this.$route.params.contestID
    this.route_name = this.$route.name
    try {
      const res = await this.$store.dispatch('getContest')
      this.changeDomTitle({ title: res.data.data.title })
      const data = res.data.data
      this.contest = data
    } catch (err) {
    }
    this.getContestProblems()
  },
  methods: {
    async getContestProblems () {
      try {
        if (this.contest.is_bank) {
          const res = await api.getProblemBankParticipation(this.contestID)
          if (!res.data.data) {
            return
          }
        }
        this.contestProblems = await this.$store.dispatch(
          this.contest.is_bank ? 'getProblemBankContestProblems' : 'getContestProblems'
        ).then((x) => x.data.data)
        this.total = this.contestProblems.length
      } catch (err) {
      }
    },
    async goContestProblem (row) {
      await this.$router.push({
        name: 'contest-problem-details',
        params: {
          contestID: this.$route.params.contestID,
          problemID: row._id,
          bank: this.contest.is_bank
        }
      })
    },
    ...mapActions(['changeDomTitle']),
    async handleRoute (route) {
      await this.$router.push(route)
    },
    async startProblemBankContest (item) {
      await api.startProblemBankContest(item.id)
      await this.getContestProblems()
    }
  },
  computed: {
    ...mapState({
      contest: state => state.contest.contest,
      problems: state => state.contest.contestProblems,
      now: state => state.contest.now
    }),
    showProblemBankStartBtn () {
      return this.contest.is_bank && !this.total
    }
  },
  watch: {
    '$route' (newVal) {
      this.route_name = newVal.name
      this.contestID = newVal.params.contestID
      this.changeDomTitle({ title: this.contest.title })
    }
  },
  beforeDestroy () {
    clearInterval(this.timer)
    this.$store.commit(types.CLEAR_CONTEST)
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
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
